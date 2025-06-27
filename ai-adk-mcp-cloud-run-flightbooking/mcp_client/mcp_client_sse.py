import asyncio
import google.auth.transport.requests
import google.oauth2.id_token
from mcp import ClientSession
from mcp.client.sse import sse_client

async def run():
    AUDIENCE = "https://mcp-server-flight-booking-service-<replace>.us-central1.run.app/"
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, AUDIENCE)

    async with sse_client(url="https://mcp-server-flight-booking-service-<replace>.us-central1.run.app/sse/",
     headers={"Authorization": f"Bearer {id_token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
            }) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            # Listing tools
            tools = await session.list_tools()
            for tp in tools:
                if tp[0] == "tools":  # Iterator of tuples ("meta", "") ("cursor", "") ("tools", ToolList)
                    for tool in tp[1]:
                        print(f"{tool.name} - {tool.description}")

            # Listing Resources
            resource_templates = await session.list_resource_templates()
            for tp in resource_templates:
                if tp[0] == "resourceTemplates":  # Iterator of tuples ("meta", "") ("cursor", "") ("resourceTemplates", Resource List)
                    for resource in tp[1]:
                        print(f"{resource.name} - {resource.description}")


            """
            # Create booking example
            # https://github.com/modelcontextprotocol/python-sdk/blob/f2f4dbdcbd30fd00ced777fd1f59d00624362c97/src/mcp/types.py#L797
            result = await session.call_tool("create_booking", arguments={"user_id": "user_1", 
                "from_location": "Denver", 
                "to_location": "Houston",
                "flight_date": "2025-05-24 15:00:00"
                })
            print(result.content[0].text)
            """
            

            """
            # Get booking example
            # https://github.com/modelcontextprotocol/python-sdk/blob/f2f4dbdcbd30fd00ced777fd1f59d00624362c97/src/mcp/types.py#L492
            booking_id = "bc301548-6192-4bed-a539-1d90436d1d08"
            result = await session.read_resource(f"flights://booking/get/{booking_id}")
            print(result.contents[0].text)
            """

            """
            # List booking example
            # https://github.com/modelcontextprotocol/python-sdk/blob/f2f4dbdcbd30fd00ced777fd1f59d00624362c97/src/mcp/types.py#L492
            user_id = "user_1"
            result = await session.read_resource(f"flights://booking/list/{user_id}")
            print(result.contents[0].text)
            """

            """
            # Cancel booking example
            # https://github.com/modelcontextprotocol/python-sdk/blob/f2f4dbdcbd30fd00ced777fd1f59d00624362c97/src/mcp/types.py#L797
            result = await session.call_tool("cancel_booking", arguments={"booking_id": "d7a4f559-155d-4d78-b2a1-befd2476b9b1"})
            print(result.content[0].text)
            """
            
if __name__ == "__main__":
    asyncio.run(run())
