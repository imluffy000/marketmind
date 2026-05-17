from langgraph.graph import StateGraph, START, END
from state import MarketMindState
from agents.price_agent import price_agent
from agents.sentiment_agent import sentiment_agent
from agents.onchain_agent import onchain_agent
from agents.macro_agent import macro_agent
from agents.risk_agent import risk_agent
from agents.synthesis_agent import synthesis_agent

workflow = StateGraph(MarketMindState)

workflow.add_node("price", price_agent)
workflow.add_node("sentiment", sentiment_agent)
workflow.add_node("onchain", onchain_agent)
workflow.add_node("macro", macro_agent)
workflow.add_node("risk", risk_agent)
workflow.add_node("synthesis", synthesis_agent)

workflow.add_edge(START, "price")
workflow.add_edge(START, "sentiment")
workflow.add_edge(START, "onchain")
workflow.add_edge(START, "macro")
workflow.add_edge(START, "risk")

workflow.add_edge("price", "synthesis")
workflow.add_edge("sentiment", "synthesis")
workflow.add_edge("onchain", "synthesis")
workflow.add_edge("macro", "synthesis")
workflow.add_edge("risk", "synthesis")

workflow.add_edge("synthesis", END)

app = workflow.compile()
