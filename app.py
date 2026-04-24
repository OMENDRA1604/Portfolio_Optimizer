from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
import os

app = Flask(__name__, static_folder='static')

# ──────────────────────────────────────────────
#  Core strategy functions
# ──────────────────────────────────────────────

def equal_weight(n):
    return [1 / n] * n


def minimum_variance(hist_return, bound):
    n = len(hist_return.columns)
    cov = hist_return.cov()

    def port_std(w):
        return np.sqrt(np.dot(w.T, np.dot(cov, w)) * 250)

    result = minimize(
        fun=port_std,
        x0=[1 / n] * n,
        bounds=[bound] * n,
        constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        method='SLSQP'
    )
    return list(result['x'])


def max_sharpe(hist_return, bound):
    n = len(hist_return.columns)
    mean = hist_return.mean(axis=0).values
    cov = hist_return.cov().values

    def neg_sharpe(w):
        ret = np.dot(w, mean) * 250
        std = np.sqrt(np.dot(w.T, np.dot(cov, w)) * 250)
        return -ret / std if std != 0 else 0

    result = minimize(
        fun=neg_sharpe,
        x0=[1 / n] * n,
        bounds=[bound] * n,
        constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        method='SLSQP'
    )
    return list(result['x'])


def portfolio_return(weights, mean_values):
    return float(np.dot(weights, mean_values) * 250)


def portfolio_std(weights, cov):
    return float(np.sqrt(np.dot(weights, np.dot(cov, weights)) * 250))


# ──────────────────────────────────────────────
#  Routes
# ──────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    tickers = [t.strip().upper() for t in data.get('tickers', [])]
    start_date = data.get('start_date', '2018-01-01')
    end_date = data.get('end_date', '2023-12-31')
    total_balance = float(data.get('total_balance', 10000))
    allow_shorting = data.get('allow_shorting', False)
    bound = (-1, 1) if allow_shorting else (0, 1)

    if len(tickers) < 2:
        return jsonify({'error': 'Please provide at least 2 tickers.'}), 400

    try:
        raw = yf.download(tickers=tickers, start=start_date, end=end_date, progress=False)
        hist_prices = raw['Close']
        if isinstance(hist_prices.columns, pd.MultiIndex):
            hist_prices.columns = hist_prices.columns.droplevel(0)
        hist_prices = hist_prices.dropna()

        if hist_prices.empty or len(hist_prices) < 30:
            return jsonify({'error': 'Not enough data. Check tickers or date range.'}), 400

        hist_return = np.log(hist_prices / hist_prices.shift()).dropna()
        hist_mean = hist_return.mean(axis=0).values
        hist_cov = hist_return.cov().values

        # Compute strategies
        ew = np.array(equal_weight(len(tickers)))
        gmv = np.array(minimum_variance(hist_return, bound))
        ms = np.array(max_sharpe(hist_return, bound))

        def build_result(weights, name):
            ret = portfolio_return(weights, hist_mean)
            std = portfolio_std(weights, hist_cov)
            sharpe = ret / std if std != 0 else 0
            allocation = {tickers[i]: round(float(weights[i]) * 100, 2) for i in range(len(tickers))}
            dollar_alloc = {tickers[i]: round(float(weights[i]) * total_balance, 2) for i in range(len(tickers))}
            return {
                'name': name,
                'weights': allocation,
                'dollars': dollar_alloc,
                'annual_return': round(ret * 100, 2),
                'annual_volatility': round(std * 100, 2),
                'sharpe_ratio': round(sharpe, 4),
            }

        strategies = [
            build_result(ew, 'Equal Weight'),
            build_result(gmv, 'Min Variance'),
            build_result(ms, 'Max Sharpe'),
        ]

        # Efficient Frontier (50 points)
        min_ret = float(np.min(hist_mean) * 250)
        max_ret = float(np.max(hist_mean) * 250) * 1.1
        target_returns = np.linspace(max(min_ret, 0.01), min(max_ret, 0.5), 50)
        frontier = []
        for target in target_returns:
            try:
                opt = minimize(
                    fun=lambda w: portfolio_std(w, hist_cov),
                    x0=ew,
                    bounds=[bound] * len(tickers),
                    constraints=(
                        {'type': 'eq', 'fun': lambda w: portfolio_return(w, hist_mean) - target},
                        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
                    ),
                    method='SLSQP'
                )
                if opt.success:
                    frontier.append({'x': round(opt['fun'] * 100, 4), 'y': round(target * 100, 4)})
            except Exception:
                pass

        # Monte Carlo portfolios (500 random)
        monte_carlo = []
        for _ in range(500):
            w = np.random.rand(len(tickers))
            w /= w.sum()
            r = portfolio_return(w, hist_mean)
            s = portfolio_std(w, hist_cov)
            monte_carlo.append({'x': round(s * 100, 3), 'y': round(r * 100, 3)})

        # Generate reasoning
        best = max(strategies, key=lambda x: x['sharpe_ratio'])
        top_asset = max(best['weights'], key=best['weights'].get)
        reasoning = (
            f"Based on data from {start_date} to {end_date}, the {best['name']} portfolio "
            f"achieves the best risk-adjusted return with a Sharpe Ratio of {best['sharpe_ratio']}. "
            f"It allocates {best['weights'][top_asset]}% to {top_asset}, which showed the strongest "
            f"risk-adjusted contribution. The portfolio targets an annual return of {best['annual_return']}% "
            f"with {best['annual_volatility']}% volatility."
        )

        return jsonify({
            'strategies': strategies,
            'frontier': frontier,
            'monte_carlo': monte_carlo,
            'reasoning': reasoning,
            'tickers': tickers,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5000)