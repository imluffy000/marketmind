import yfinance as yf
import pandas as pd
from agents import llm, safe_parse_json
from state import MarketMindState, AgentSignal

def risk_agent(state: MarketMindState) -> dict:
    ticker = state["ticker"]
    yfin_ticker = f"{ticker}-USD" if state["asset_type"] == "crypto" else ticker
    
    try:
        data = yf.download(yfin_ticker, period="1y", interval="1d", progress=False)
        if data.empty:
            return {"agent_signals": [AgentSignal(
                agent="risk", signal="NEUTRAL", confidence=0.0,
                summary=f"No data for {ticker}", raw_data={}
            )]}
            
        close = data["Close"].squeeze()
        returns = close.pct_change().dropna()
        
        # Annualized volatility
        volatility = round(float(returns.std() * (252 ** 0.5)), 4)
        
        # Max drawdown
        cumulative = (1 + returns).cumprod()
        rolling_max = cumulative.cummax()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = round(float(drawdown.min()), 4)
        
        raw_data = {
            "annualized_volatility": volatility,
            "max_drawdown": max_drawdown,
            "current_drawdown": round(float(drawdown.iloc[-1]), 4)
        }
        
        prompt = f"""You are a quantitative risk manager. Analyze this risk data for {ticker}:
        
{raw_data}

High volatility and deep drawdowns are BEARISH (high risk). Low volatility and shallow drawdowns are BULLISH (low risk).

Return ONLY valid JSON with exactly these fields:
{{"signal": "BULLISH" or "BEARISH" or "NEUTRAL", "confidence": 0.0 to 1.0, "summary": "one sentence under 20 words"}}"""

        result_raw = llm.invoke(prompt)
        result = safe_parse_json(result_raw.content)
        
        return {"agent_signals": [AgentSignal(
            agent="risk",
            signal=result["signal"],
            confidence=float(result["confidence"]),
            summary=result["summary"],
            raw_data=raw_data
        )]}
        
    except Exception as e:
        return {"agent_signals": [AgentSignal(
            agent="risk", signal="NEUTRAL", confidence=0.0,
            summary=f"Risk agent error: {str(e)[:60]}", raw_data={}
        )]}
