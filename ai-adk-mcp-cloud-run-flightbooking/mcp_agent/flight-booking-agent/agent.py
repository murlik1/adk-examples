import google.auth.transport.requests
import google.oauth2.id_token
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams
from mcp import ClientSession
from mcp.client.sse import sse_client
import asyncio
import os

# AUDIENCE = "https://mcp-server-flight-booking-service-<replace_project>.us-central1.run.app/"
# ENDPOINT = "https://mcp-server-flight-booking-service-<replace_project>.us-central1.run.app/sse/"

AUDIENCE = os.environ.get("MCP_SERVER_URL") | "/"
ENDPOINT = os.environ.get("MCP_SERVER_URL") + "/sse/"

async def get_booking(booking_id: str)-> str:
    """
    This tool is get the booking details based on the booking id provided by user.
    This tool calls the MCP tool resource to get the required details

    Args:
        booking_id : String column representing the booking id

    Returns:
        JSON String response
    """
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, AUDIENCE)

    async with sse_client(url=ENDPOINT,
     headers={"Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
            }) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            
            result = await session.read_resource(f"flights://booking/get/{booking_id}")
            print(result.contents[0].text)
            return result.contents[0].text

async def list_booking(user_id: str)-> str:
    """
    This tool is get the booking ids based on the user_id.
    This tool calls the MCP tool resource to get the required details.

    Args:
        user_id : String column representing the user_id

    Returns:
        JSON String response
    """
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, AUDIENCE)

    async with sse_client(url=ENDPOINT,
     headers={"Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
            }) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            
            result = await session.read_resource(f"flights://booking/list/{user_id}")
            print(result.contents[0].text)
            return result.contents[0].text

async def get_tools():
    """Gets tools from the File System MCP Server."""
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, AUDIENCE)

    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseConnectionParams(
            url= ENDPOINT,
            headers={ "Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
            }
        )
    )
    print("MCP Toolset created successfully.")
    return tools, exit_stack

async def create_agent_async():
    tool_list = []
    tools, exit_stack = await get_tools()
    tool_list.extend(tools)
    tool_list.extend([get_booking, list_booking])
    print(tool_list)

    flight_booking_agent = LlmAgent(name = "flight_booking_agent",
        model = "gemini-2.5-flash-preview-04-17",
        description = "This agent handles the flight bookings for the user",
        instruction = """
            You are agent that handles the flight bookings for the `user_id` user_1.
            You have access to below set of the tools for performing flight bookings

            - create_booking - Use this tool for booking the flight
                - Obtain the details like `from_location`, `to_location` and `flight_date` for calling this tool.
                - Handle the `flight_date` value to convert as string in format 'yyyy-mm-dd HH:MM:SS'
                - Respond back with the `booking_id` back to the user 
            - cancel_booking - Use this tool for cancelling a booking based on `booking_id` provided by the user
            - get_booking - Use this tool for get the booking details for given `booking_id`
            - list_booking - Use this tool for listing the booking_ids for the user based on `user_id`
        """,
        tools = tool_list
        )

    return flight_booking_agent, exit_stack

root_agent = create_agent_async()

"""
Show all my bookings
Get me booking detail for 5c530364-b18b-474f-97c5-7ab654b2d883
Cancel booking 5c530364-b18b-474f-97c5-7ab654b2d883
ok, create a new booking for me from Delhi to Mumbai on 25-06-2025
"""