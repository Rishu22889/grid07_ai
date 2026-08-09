# app/graph/langgraph_flow.py

from __future__ import annotations

import json
from typing import Any, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

from app.config.settings import GROQ_API_KEY, GROQ_MODEL
from app.personas.bot_personas import BotPersona
from app.tools.mock_search import mock_searxng_search

try:
    from app.tools.real_search import search_web

    REAL_SEARCH_AVAILABLE = True

except ImportError:
    REAL_SEARCH_AVAILABLE = False
    search_web = None

class GraphState(TypedDict):
    bot_id: str
    persona: str
    topic: str
    search_results: list[dict[str, Any]]
    post_content: str


def _get_llm(temperature: float = 0.72) -> ChatGroq:
    """Create and return the Groq LLM client."""

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=temperature,
        api_key=GROQ_API_KEY,
    )


def decide_topic(state: GraphState) -> dict[str, str]:
    """Decide on a specific topic based on the bot persona."""

    persona = state["persona"]

    system_prompt = f"""
{persona}

Task:
Decide a topic you want to post about today.

Rules:
- Topic must strongly reflect your personality.
- Avoid generic phrases like "AI powered" or "AI driven".
- Be specific and opinionated.
- Keep it short (3-6 words).

Return ONLY the topic.
""".strip()

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content="What topic do you want to post about today?"
        ),
    ]

    llm = _get_llm()

    response = llm.invoke(messages)

    topic = (
        response.content
        .strip()
        .strip('"')
        .strip("'")
    )

    return {
        "topic": topic
    }


def web_search(state: GraphState) -> dict[str, list[dict[str, Any]]]:
    """
    Search the web for information related to the selected topic.

    Uses Tavily when available.
    Falls back to mock search if Tavily is unavailable or fails.
    """

    topic = state["topic"]


    if REAL_SEARCH_AVAILABLE and search_web is not None:

        try:
            raw_results = search_web(
                topic,
                max_results=3,
            )

            results: list[dict[str, Any]] = []

            for result in raw_results:

                results.append(
                    {
                        "title": result.get("title", ""),
                        "snippet": result.get("content", "")[:500],
                        "url": result.get("url", ""),
                        "score": result.get("score", 0.0),
                    }
                )

            # Only return Tavily results if we actually
            # received something useful.
            if results:
                return {
                    "search_results": results
                }

        except Exception:
            # Fall through to mock search.
            pass

    # --------------------------------------------------------
    # Fallback: Mock Search
    # --------------------------------------------------------

    mock_results = mock_searxng_search(topic)

    results = []

    for result in mock_results:

        results.append(
            {
                "title": result.get("title", ""),
                "snippet": result.get(
                    "content",
                    result.get("snippet", ""),
                ),
                "url": result.get("url", ""),
                "score": result.get("score", 0.0),
            }
        )

    return {
        "search_results": results
    }



def draft_post(state: GraphState) -> dict[str, str]:
    """Draft a social media post using persona and search context."""

    persona = state["persona"]
    topic = state["topic"]
    search_results = state["search_results"]

    context = json.dumps(
        search_results,
        indent=2,
        ensure_ascii=False,
    )

    system_prompt = f"""
{persona}

You are writing a highly opinionated social media post.

Topic:
"{topic}"

Context from web search:
{context}

Rules:
- Strongly reflect your personality and beliefs.
- You MUST incorporate at least one insight from the context.
- Be opinionated, not neutral.
- Keep it concise: 1-2 sentences, maximum 280 characters.
- Avoid generic phrases like "AI powered" or "future of AI".
- Reference at least one specific detail from the context.
- Do NOT ignore the provided context.

Return ONLY the post content.
""".strip()

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=(
                "Draft a social media post based on "
                "the above information."
            )
        ),
    ]

    llm = _get_llm()

    response = llm.invoke(messages)

    post_content = (
        response.content
        .strip()
        .strip('"')
        .strip("'")
    )

    return {
        "post_content": post_content
    }


def build_graph():
    """Build and compile the content-generation graph."""

    workflow = StateGraph(GraphState)

    workflow.add_node(
        "decide_topic",
        decide_topic,
    )

    workflow.add_node(
        "web_search",
        web_search,
    )

    workflow.add_node(
        "draft_post",
        draft_post,
    )

    workflow.add_edge(
        START,
        "decide_topic",
    )

    workflow.add_edge(
        "decide_topic",
        "web_search",
    )

    workflow.add_edge(
        "web_search",
        "draft_post",
    )

    workflow.add_edge(
        "draft_post",
        END,
    )

    return workflow.compile()


def run_agent(bot: BotPersona) -> dict[str, str]:
    """Run the complete content-generation pipeline."""

    agent = build_graph()

    initial_state: GraphState = {
        "bot_id": bot.id,
        "persona": bot.systemPrompt,
        "topic": "",
        "search_results": [],
        "post_content": "",
    }

    result = agent.invoke(initial_state)

    return {
        "bot_id": result["bot_id"],
        "topic": result["topic"],
        "post_content": result["post_content"],
    }