import os
import uvicorn
import uuid
from typing import Union, Dict, List, Any
from fastmcp import FastMCP, Context
from google.cloud import bigquery

# Creation of MCP Server
mcp = FastMCP("flight_booking_mcp_server")

PROJECT = os.environ.get("PROJECT", "<replace>")
DATASET = os.environ.get("DATASET", "flight_ds")
TABLE = os.environ.get("TABLE", "flight_bookings")

@mcp.tool(
    name="create_booking",
    description="This is a MCP tool for creating flight booking"
)
def create_booking(user_id: str,
    from_location: str,
    to_location: str,
    flight_date: str,
    ctx: Context
    ) -> Union[Dict[str, Any], None]:
    """
    This function creates flight booking (record) in bigquery table flight_bookings.

    Args:
        user_id: string representing id of the user
        from_location: string representing starting location of the flight
        to_location: string representing end location of the flight
        flight_date: string representing date of the flight
    
    Returns:
        String representing the booking id.
    """

    client = bigquery.Client(project=PROJECT)
    table = f"{PROJECT}.{DATASET}.{TABLE}"

    booking_id = str(uuid.uuid4())

    query_text = f"""
    insert into `{table}` values ('{user_id}', '{booking_id}', '{from_location}', '{to_location}', '{flight_date}', "Active")
    """

    query_job = client.query(query_text)

    query_job.result()

    if query_job.num_dml_affected_rows is not None:
        ctx.info(f"[create_booking]: Booking id {booking_id} created")
        return {"booking_id": booking_id}
    else:
        ctx.error(f"[create_booking]: Booking Creation Failed")
        return None


@mcp.tool(
    name="cancel_booking",
    description="This is a MCP tool for cancelling flight booking"
)
def cancel_booking(booking_id: str,
    ctx: Context
    ) -> str:
    """
    This function helps to cancel flight booking  by updating the booking status as "Cancelled" in the bigquery table

    Args:
        booking_id: string booking_id
    
    Returns:
        String representing the status
    """

    client = bigquery.Client(project=PROJECT)
    table = f"{PROJECT}.{DATASET}.{TABLE}"

    query_text = f"""
        MERGE INTO `{table}` tgt
        using (select '{booking_id}' as booking_id) src
        on tgt.booking_id = src.booking_id
        when matched then update set booking_status = "Cancelled"
    """

    query_job = client.query(query_text)

    query_job.result()

    if query_job.num_dml_affected_rows is not None:
        ctx.info(f"[cancel_booking]: booking id {booking_id} is cancelled, Rows affected - {query_job.num_dml_affected_rows}")
        return f"[cancel_booking]: booking id {booking_id} is cancelled, Rows affected - {query_job.num_dml_affected_rows}"
    else:
        ctx.info(f"[cancel_booking]: booking id {booking_id} is not found")
        return f"[cancel_booking]: booking id {booking_id} is not found"

@mcp.resource(
    name = "get_booking",
    uri = "flights://booking/get/{booking_id}",
    description= "This MCP resource retrieves the booking details mentioned by booking id"
)
def get_booking(booking_id:str, ctx: Context) -> Union[List[Dict[str, Any]], None]:
    """
    This function helps to retrieve flight booking details based on the booking id

    Args:
        booking_id: string booking_id
    
    Returns:
        List of Dictionary representing the booking information for the booking id
    """

    client = bigquery.Client(project=PROJECT)
    table = f"{PROJECT}.{DATASET}.{TABLE}"

    query_text = f"""
        SELECT *
        from `{table}`
        WHERE booking_id = "{booking_id}"
    """

    query_job = client.query(query_text)
    query_list = []

    for row in query_job:
        query_list.append(dict(row.items()))

    ctx.info(f"[get_booking]: retrieved {len(query_list)} records for booking id {booking_id}")

    return query_list

@mcp.resource(
    name = "list_booking",
    uri = "flights://booking/list/{user_id}",
    description= "This MCP resource retrieves the booking details mentioned by booking id"
)
def list_booking(user_id: str, ctx: Context) -> Union[List[Dict[str, Any]], None]:
    """
    This function helps to retrieve flight booking ids based on the user id

    Args:
        user_id: string booking_id
    
    Returns:
        List of Dictionary representing the booking information for the user id
    """

    client = bigquery.Client(project=PROJECT)
    table = f"{PROJECT}.{DATASET}.{TABLE}"

    query_text = f"""
        SELECT distinct booking_id
        from `{table}`
        WHERE user_id = "{user_id}"
    """

    query_job = client.query(query_text)
    query_list = []

    for row in query_job:
        query_list.append(dict(row.items()))

    ctx.info(f"[list_booking]: retrieved {len(query_list)} records for user id {user_id}")
    
    return query_list

# Register uvicorn app as SSE application
sse_app = mcp.sse_app()

if __name__ == "__main__":
    uvicorn.run(sse_app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))