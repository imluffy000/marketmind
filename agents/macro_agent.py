import os
import json
import requests
from agents import llm, safe_parse_json
from state import MarketMindState, AgentSignal

def fetch_fred(series_id: str, api_key: str, limit: int = 5) -> list:
    """Fetch recent values from a FRED economic data series."""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id, "api_key": api_key,
        "file_type": "json", "sort_order": "desc", "limit": limit,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    # FRED uses "." as placeholder for missing/unreleased data - filter those out
    return [
        {"date": o["date"], "value": round(float(o["value"]), 4)}
        for o in resp.json().get("observations", [])
        if o["value"] != "."
    ]

def macro_agent(state: MarketMindState) -> dict:
    # Macro data affects all assets similarly in this simple model
    try:
        api_key = os.getenv("FRED_API_KEY")
        if not api_key:
            return {"agent_signals": [AgentSignal(
                agent="macro", signal="NEUTRAL", confidence=0.3,
                summary="FRED API key not found", raw_data={}
            )]}
            
        # 10-Year Treasury Yield (Risk-free rate proxy)
        # DGS10 is daily
        rates = fetch_fred("DGS10", api_key)
        
        # Core Inflation (PCE) - Monthly
        # PCEPILFE is monthly
        inflation = fetch_fred("PCEPILFE", api_key, limit=2)
        
        # VIX (Volatility Index) - Daily
        # VIXCLS is daily
        vix = fetch_fred("VIXCLS", api_key)
        
        raw_data = {
            "10y_treasury_yield": rates,
            "core_inflation": inflation,
            "vix": vix,
        }
        
        prompt = f"""You are a macroeconomic strategist. Analyze this recent US economic data:
        
{json.dumps(raw_data, indent=2)}

Determine the current macro environment's impact on risk assets (like stocks and crypto).
High rates/inflation/VIX are generally BEARISH. Decreasing rates/inflation/VIX are generally BULLISH.

Return ONLY valid JSON with exactly these fields:
{{"signal": "BULLISH" or "BEARISH" or "NEUTRAL", "confidence": 0.0 to 1.0, "summary": "one sentence under 20 words"}}"""

        result_raw = llm.invoke(prompt)
        result = safe_parse_json(result_raw.content)
        
        return {"agent_signals": [AgentSignal(
            agent="macro",
            signal=result["signal"],
            confidence=float(result["confidence"]),
            summary=result["summary"],
            raw_data=raw_data
        )]}
        
    except Exception as e:
        return {"agent_signals": [AgentSignal(
            agent="macro", signal="NEUTRAL", confidence=0.0,
            summary=f"Macro agent error: {str(e)[:60]}", raw_data={}
        )]}
