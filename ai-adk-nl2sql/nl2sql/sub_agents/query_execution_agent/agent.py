from google.adk.agents import LlmAgent
from nl2sql.sub_agents.query_execution_agent.prompts import QUERY_EXECUTION_INSTRUCTION_STR
from nl2sql.tools.bigquery_tools import bigquery_execution_tool

# LLM Agent for execution of the bigquery sqls
query_execution_agent = LlmAgent(
    name = "query_execution_agent",
    model = "gemini-2.5-flash",
    description = f"This agent is responsible for exeuction of queries in the bigquery and present the result as markdown table",
    instruction = QUERY_EXECUTION_INSTRUCTION_STR,
    tools = [ bigquery_execution_tool ],
    output_key = "query_execution_output"
)