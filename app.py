import streamlit as st
from graph import app as market_graph

st.set_page_config(page_title="MarketMind AI", layout="wide")

st.title("🧠 MarketMind AI")
st.write("A multi-agent system for analyzing market conditions.")

col1, col2 = st.columns(2)
with col1:
    ticker = st.text_input("Ticker Symbol (e.g. AAPL, BTC)", value="BTC")
with col2:
    asset_type = st.selectbox("Asset Type", ["crypto", "stock"])

if st.button("Run Analysis"):
    with st.spinner(f"Agents are analyzing {ticker}..."):
        initial_state = {
            "ticker": ticker,
            "asset_type": asset_type,
            "agent_signals": []
        }
        
        final_state = market_graph.invoke(initial_state)
        
        st.subheader("Final Verdict")
        
        verdict = final_state.get("final_verdict", "NEUTRAL")
        color = "green" if verdict == "BULLISH" else "red" if verdict == "BEARISH" else "gray"
        
        st.markdown(f"<h3 style='color: {color}'>{verdict} (Confidence: {final_state.get('final_confidence', 0):.2f})</h3>", unsafe_allow_html=True)
        st.write(f"**Reasoning:** {final_state.get('final_reasoning', '')}")
        
        st.divider()
        st.subheader("Agent Breakdown")
        
        signals = final_state.get("agent_signals", [])
        
        for s in signals:
            with st.expander(f"{s['agent'].upper()} Agent - {s['signal']} (Conf: {s['confidence']})"):
                st.write(f"**Summary:** {s['summary']}")
                st.write("**Raw Data:**")
                st.json(s.get("raw_data", {}))
