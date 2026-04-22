# LangGraph flow (Phase 2)
# app/graph/langgraph_flow.py

from __future__ import annotations
from typing import Any, TypedDict
import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph import graph
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from app.config.settings import GROQ_MODEL, GROQ_API_KEY
from app.personas.bot_personas import BotPersona
from app.tools.mock_search import mock_searxng_search


class graphState(TypedDict):
    bot_id: str
    persona: str
    topic: str
    search_results: list[str]
    post_content: str

def _get_llm(temperature: float = 0.72) -> ChatGroq:
    return ChatGroq(model=GROQ_MODEL, temperature=temperature, api_key=GROQ_API_KEY)


def decide_topic(state: graphState) -> str:
    """This function decides on a specific topic for the bot to post about, based on its persona."""
    persona = state['persona']
    system_prompt = (
        f"""{persona}
        Task:
        Decide a topic you want to post about today.

        Rules:
        - Topic must reflect your personality strongly
        - Avoid generic phrases like "AI powered", "AI driven"
        - Be specific and opinionated
        - Keep it short (3-6 words)

        Return ONLY the topic."""
    )

    message = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="What topic do you want to post about today?")
    ]

    llm = _get_llm()
    response = llm.invoke(message)
    topic = response.content.strip().strip('"').strip("'")
    return {"topic": topic}

# Note: In a real implementation, this mock tool can be replaced with a real search API like SearxNG or Tavily.

def web_search(state: graphState):
    """This function performs mock web search to retrieve relevant information about the topic."""

    topic = state["topic"]

    results = mock_searxng_search(topic)

    return {"search_results": results}

def draft_post(state: graphState):
    """This function drafts a social media post based on the bot's persona, the chosen topic, and the search results."""
    persona = state['persona']
    topic = state['topic']
    search_results = state['search_results']

    system_prompt = f"""
        {persona}

        You are writing a highly opinionated social media post.

        Topic: "{topic}"

        Context (MUST USE):
        {json.dumps(search_results, indent=2)}

        Rules:
        - Strongly reflect your personality and beliefs
        - You MUST incorporate at least one insight from the context
        - Be opinionated, not neutral
        - Keep it concise (1-2 sentences, max 280 chars)
        - Avoid generic phrases like "AI powered", "future of AI"
        - You MUST reference a specific detail from the context
        - Do NOT ignore the context

        Return ONLY the post content.
        """

    message = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Draft a social media post based on the above information.")
    ]

    llm = _get_llm()
    response = llm.invoke(message)
    post_content = response.content.strip().strip('"').strip("'")
    return {"post_content": post_content}

def build_graph():
    graph = StateGraph(graphState)

    graph.add_node("decide_topic", decide_topic)
    graph.add_node("web_search", web_search)
    graph.add_node("draft_post", draft_post)

    graph.add_edge(START, "decide_topic")
    graph.add_edge("decide_topic", "web_search")
    graph.add_edge("web_search", "draft_post")
    graph.add_edge("draft_post", END)

    return graph.compile()


def run_agent(bot: BotPersona):
    agent = build_graph()

    initial_state: graphState = {
        "bot_id": bot.id,
        "persona": bot.systemPrompt,
        "topic": "",
        "search_results": [],
        "post_content": ""
    }

    result = agent.invoke(initial_state)
    return {"bot_id": result["bot_id"], "topic": result["topic"] , "post_content": result["post_content"]}

