"""
LangGraph workflow definition.
Creates the StateGraph that processes user messages through the AI pipeline.

Flow:
    User Message → Intent Detection → Tool Execution → Response Generation
"""

from typing import Optional
from langgraph.graph import StateGraph, END

from app.graph.state import AgentState
from app.graph.nodes import intent_node, tool_node, response_node
from app.graph.router import route_to_tool
from app.utils.logger import get_logger

logger = get_logger(__name__)


def should_use_tool(state: AgentState) -> str:
    """Conditional edge: decide whether to use a tool or go straight to response."""
    intent = state.get("intent", "general")
    if intent in ("log", "edit", "summarize", "followup", "lookup"):
        return "tool_node"
    return "response_node"


def build_graph() -> StateGraph:
    """
    Build the LangGraph workflow.
    
    Graph structure:
        START → intent_node → (conditional) → tool_node → response_node → END
                                            └→ response_node → END
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("intent_node", intent_node)
    workflow.add_node("tool_node", tool_node)
    workflow.add_node("response_node", response_node)

    # Set entry point
    workflow.set_entry_point("intent_node")

    # Add conditional edge from intent to tool or response
    workflow.add_conditional_edges(
        "intent_node",
        should_use_tool,
        {
            "tool_node": "tool_node",
            "response_node": "response_node",
        },
    )

    # Tool node always goes to response node
    workflow.add_edge("tool_node", "response_node")

    # Response node ends the graph
    workflow.add_edge("response_node", END)

    return workflow.compile()


# Singleton compiled graph
_compiled_graph = None


def get_graph():
    """Get or create the compiled LangGraph."""
    global _compiled_graph
    if _compiled_graph is None:
        logger.info("Building LangGraph workflow...")
        _compiled_graph = build_graph()
        logger.info("LangGraph workflow compiled successfully")
    return _compiled_graph
