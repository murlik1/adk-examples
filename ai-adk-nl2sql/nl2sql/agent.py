from google.adk.agents import LlmAgent, BaseAgent
from nl2sql.sub_agents.query_understanding_agent.agent import query_understanding_agent
from nl2sql.sub_agents.query_generation_agent.agent import query_generation_agent
from nl2sql.sub_agents.query_review_rewrite_agent.agent import query_review_rewrite_agent
from nl2sql.sub_agents.query_execution_agent.agent import query_execution_agent
from nl2sql.tools.initialize_state import initialize_state_var

from typing import Dict, Any, List
from typing import AsyncGenerator
from typing_extensions import override
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools import ToolContext
import logging

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Orchestrator Agent
class OrchestratorAgent(BaseAgent):
    query_understanding_agent: LlmAgent
    query_generation_agent: LlmAgent
    query_review_rewrite_agent: LlmAgent
    query_execution_agent: LlmAgent

    def __init__(self,
        name:str,
        query_understanding_agent: LlmAgent,
        query_generation_agent: LlmAgent,
        query_review_rewrite_agent: LlmAgent,
        query_execution_agent:LlmAgent):
        
        super().__init__(
            name = name,
            query_understanding_agent = query_understanding_agent,
            query_generation_agent = query_generation_agent,
            query_review_rewrite_agent = query_review_rewrite_agent,
            query_execution_agent=query_execution_agent,
            before_agent_callback=initialize_state_var,
            description = "This is a Orchestrator Agent which executes the nl2sql workflow using the sub_agents provided"
        )

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        logger.info(f"[{self.name}] - Starting nl2sql workflow.")

        # First call to query_understanding_agent
        async for event in self.query_understanding_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        query_understanding_output = ""
        if "query_understanding_output" in ctx.session.state:
            query_understanding_output = ctx.session.state['query_understanding_output']
            logger.info(f"[{self.name}] - {query_understanding_output}")

        if query_understanding_output is None or "```json" not in query_understanding_output:
            return
        
        # query generation agent call
        async for event in self.query_generation_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        query_generation_output = ctx.session.state['query_generation_output']
        logger.info(f"[{self.name}] - {query_generation_output}")

        if query_generation_output is None:
            return

        # query review rewrite agent call
        async for event in self.query_review_rewrite_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        query_review_rewrite_output = ctx.session.state['query_review_rewrite_output']
        logger.info(f"[{self.name}] - {query_review_rewrite_output}")

        if query_review_rewrite_output is None:
            return
        
        # query execution agent call
        async for event in self.query_execution_agent.run_async(ctx):
            logger.info(f"[{self.name}] - {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        
        query_execution_output = ctx.session.state['query_execution_output']
        logger.info(f"[{self.name}] - {query_execution_output}")

        if query_execution_output is None:
            return

orchestrator_agent = OrchestratorAgent(name="orchestrator_agent",
    query_understanding_agent=query_understanding_agent,
    query_generation_agent=query_generation_agent,
    query_review_rewrite_agent=query_review_rewrite_agent,
    query_execution_agent=query_execution_agent
    )

root_agent = orchestrator_agent

"""
Fetch me count of orders as per status for orders placed on 15-05-2025
Fetch me orders that are in cancelled state on 15-05-2025
Fetch me the products most ordered in 2025
Fetch me the top selling product in 2025 as per number of orders placed
Fetch me product with highest available inventory
"""