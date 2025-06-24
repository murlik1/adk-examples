from google.adk.agents import LlmAgent
from nl2sql.sub_agents.query_understanding_agent.prompts import QUERY_UNDERSTANDING_PROMPT_STR

# LLM Agent for analysis of the user query to identify the user question and derive tables/columns involved 
query_understanding_agent = LlmAgent(
    name = "query_understanding_agent",
    model = "gemini-2.5-flash",
    description = """This agent is responsible for understanding the intent of the user question 
        and identifying tables/columns involved to answer the query
    """,
    instruction = QUERY_UNDERSTANDING_PROMPT_STR,
    output_key = "query_understanding_output"
)