import os
from pydantic_ai import Agent
from apps.assistant.agents.context import AssistantContext
from apps.assistant.agents.prompts import DANDI_ASSISTANT_SYSTEM_PROMPT
from apps.assistant.tools.article_search_tool import search_dandi_articles


def create_dandi_agent() -> Agent[AssistantContext, str]:
    """
    Factory function to initialize and configure Dandi AI Agent with Groq LLM and tools.
    """
    raw_model = os.getenv('GROQ_MODEL', 'qwen/qwen3.8-27b').strip()
    model_identifier = f"groq:{raw_model}" if not raw_model.startswith("groq:") else raw_model

    agent = Agent(
        model_identifier,
        deps_type=AssistantContext,
        system_prompt=DANDI_ASSISTANT_SYSTEM_PROMPT,
    )

    # Register the article search tool for recommendations
    agent.tool(search_dandi_articles)

    return agent


# Global agent instance for reuse
dandi_agent = create_dandi_agent()
