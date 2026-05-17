# you can access the application using : https://marketmind0.streamlit.app/

# 🧠 MarketMind AI

MarketMind AI is a powerful, multi-agent financial analysis system built with **LangGraph**, **Streamlit**, and **Groq** (running Llama 3 models). It utilizes a parallel fan-out architecture where multiple specialist AI agents concurrently analyze different dimensions of an asset (both stocks and crypto), before a lead synthesis agent evaluates all signals to generate a final trading verdict.

## 🚀 Features

- **Multi-Agent Architecture**: Uses `langgraph` to run 5 specialized agents in parallel, preventing bottlenecks.
- **Support for Stocks & Crypto**: Analyzes both traditional equities and cryptocurrencies using unified logic.
- **Interactive Dashboard**: A clean, responsive Streamlit web interface to view both the final verdict and the granular breakdowns from each agent.
- **Fast Inference**: Powered by Groq's blazing-fast inference engine running Llama-3.3-70b.

## 🤖 The Agents

1. **Price Agent**: Analyzes technical indicators including RSI, MACD crossovers, and Bollinger Bands using `yfinance` data.
2. **Sentiment Agent**: Fetches the latest global news via `NewsAPI` and performs financial sentiment analysis to determine market mood.
3. **On-Chain / Microstructure Agent**: Uses `CoinGecko` for cryptocurrency metrics (volume-to-market-cap ratio, ATH changes) and `yfinance` for traditional equities (short ratios, beta).
4. **Macro Agent**: Pulls real-time macroeconomic indicators (10Y Treasury Yield, Core PCE Inflation, VIX) directly from the St. Louis Fed (`FRED API`) to assess the broader risk environment.
5. **Risk Agent**: Computes rolling metrics such as annualized volatility and maximum drawdown to assess the downside risk.
6. **Synthesis Agent**: The lead portfolio manager that reviews the structured JSON outputs of all 5 agents, weighs their confidence scores, and produces a final bullish/bearish/neutral verdict with reasoning.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/imluffy000/marketmind.git
   cd marketmind
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Run:
   ```bash
   pip install langgraph langchain-groq python-dotenv yfinance pandas pycoingecko newsapi-python requests streamlit
   ```

3. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add the following API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   NEWS_API_KEY=your_newsapi_key_here
   FRED_API_KEY=your_fred_api_key_here
   ```

## 🎮 Usage

Start the Streamlit dashboard by running:

```bash
streamlit run app.py
```

1. Enter a **Ticker Symbol** (e.g., `BTC`, `AAPL`, `TSLA`).
2. Select the **Asset Type** (`crypto` or `stock`).
3. Click **Run Analysis** to trigger the LangGraph workflow.
4. Review the final verdict, confidence score, and the expandable breakdowns from each specialized agent.

## 📁 Project Structure

```text
marketmind/
├── .env                  # API Keys (Git ignored)
├── state.py              # Shared TypedDict state definitions
├── graph.py              # LangGraph parallel fan-out workflow
├── app.py                # Streamlit UI dashboard
└── agents/               # Specialist Agent Logic
    ├── __init__.py       # Groq client & JSON parser utilities
    ├── price_agent.py    # Technical analysis agent
    ├── sentiment_agent.py# News sentiment agent
    ├── onchain_agent.py  # Market microstructure agent
    ├── macro_agent.py    # Macroeconomic environment agent
    ├── risk_agent.py     # Volatility & drawdown agent
    └── synthesis_agent.py# Final portfolio manager agent
```

## ⚠️ Disclaimer

**This tool is for educational and informational purposes only.** The AI-generated verdicts should not be considered financial advice. Always do your own research (DYOR) before making investment decisions.
