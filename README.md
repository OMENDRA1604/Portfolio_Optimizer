# 📊 Portfolio Optimizer

A powerful web application that helps users build optimal investment portfolios using **Modern Portfolio Theory (MPT)**.
It analyzes historical stock data and provides optimized allocations based on different strategies like **Minimum Variance** and **Maximum Sharpe Ratio**.

<img width="974" height="647" alt="WhatsApp Image 2026-04-25 at 9 42 36 AM" src="https://github.com/user-attachments/assets/84740b40-f3af-403e-b749-872a2e96cd8c" />

---

## 🚀 Live Demo

👉 [Portfolio Optimizer](https://portfolio-optimizer-zito.onrender.com)

---

## 🧠 Features

* 📈 **Portfolio Optimization Strategies**

  * Equal Weight Portfolio
  * Minimum Variance Portfolio (Lowest Risk)
  * Maximum Sharpe Ratio Portfolio (Best Risk-Adjusted Return)

* 📊 **Efficient Frontier Visualization**

  * Shows optimal risk-return combinations

* 🎯 **Monte Carlo Simulation**

  * Generates random portfolios for comparison

* 💡 **AI-like Reasoning**

  * Explains which portfolio is best and why

* 🌐 **Real-time Market Data**

  * Fetches stock data using Yahoo Finance API

---

## 🛠 Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* Python
* Flask

**Libraries & Tools**

* NumPy
* Pandas
* SciPy
* yFinance

---

## 📂 Project Structure

```
Portfolio_Optimizer/
│
├── app.py                # Flask backend
├── requirements.txt     # Dependencies
├── Procfile             # Deployment config (Render)
├── static/
│   ├── index.html       # Frontend UI
│   ├── style.css
│   └── script.js
```

---

## ⚙️ How It Works

1. User enters stock tickers (e.g., AAPL, MSFT, GOOG)
2. App fetches historical price data
3. Calculates:

   * Returns
   * Covariance matrix
4. Runs optimization algorithms:

   * Min Variance
   * Max Sharpe
5. Displays:

   * Allocation
   * Risk (Volatility)
   * Return
   * Sharpe Ratio

---

## 🧪 Example Input

```json
{
  "tickers": ["AAPL", "MSFT", "GOOG"],
  "total_balance": 10000
}
```

---

## 📊 Output Example

* Optimal allocation (% and $)
* Expected annual return
* Risk (volatility)
* Sharpe ratio
* Efficient frontier graph

---

## ⚡ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/OMENDRA1604/Portfolio_Optimizer.git
cd Portfolio_Optimizer
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the app

```
python app.py
```

### 5. Open in browser

```
http://localhost:5000
```

---

## 🌍 Deployment

Deployed using **Render**

### Steps:

* Connect GitHub repo
* Add build command:

```
pip install -r requirements.txt
```

* Start command:

```
python app.py
```

---

## ⚠️ Limitations

* Depends on Yahoo Finance API (may be slow or rate-limited)
* No user authentication
* No portfolio persistence (yet)

---

## 🔮 Future Improvements

* 🔐 User login & saved portfolios
* 📊 Interactive charts (Chart.js / D3.js)
* ⚡ Caching for faster responses
* 🤖 ML-based portfolio suggestions
* 🌐 Multi-asset support (crypto, ETFs)

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Omendra Singh**
🔗 GitHub: https://github.com/OMENDRA1604

---

## ⭐ If you like this project

Give it a star ⭐ and share it!




