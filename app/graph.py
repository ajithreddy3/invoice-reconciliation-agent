from langgraph.graph import StateGraph
from utils.schemas import AgentState
from agents.document_agent import document_agent
from agents.matching_agent import matching_agent
from agents.discrepancy_agent import discrepancy_agent
from agents.resolution_agent import resolution_agent

graph = StateGraph(AgentState)

graph.add_node("document", document_agent)
graph.add_node("match", matching_agent)
graph.add_node("discrepancy", discrepancy_agent)
graph.add_node("resolution", resolution_agent)

graph.set_entry_point("document")
graph.add_edge("document", "match")
graph.add_edge("match", "discrepancy")
graph.add_edge("discrepancy", "resolution")

app = graph.compile()
