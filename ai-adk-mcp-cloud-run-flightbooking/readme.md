# Table Creation
```
create schema `<replace_project>`.flight_demo_ds
create or replace table `<replace_project>.flight_demo_ds.flight_bookings`
(
  user_id string,
  booking_id string,
  from_location string,
  to_location string,
  flight_date datetime,
  booking_status string
);
```

# MCP Local Server Execution
```
cd ~/adk-examples/adk-nl2sql/ai-adk-mcp-cloud-run-flightbooking
python main.py
```


# Deploy MCP Server to Cloud Run
```
gcloud run deploy mcp-server-flight-booking-service
--source . \
--region us-central1 \
--port=8080 \
--no-allow-unauthenticated \
--set-env-vars="PROJECT=<Initiate>,DATASET=<Initiate>,TABLE=<Initiate>"
```

# Optional Steps to build image seperately and deploy to cloud run
```
gcloud auth configure-docker us-central1-docker.pkg.dev

create a artifact registry [Docker] - docker-repo

docker build . -t us-central1-docker.pkg.dev/<replace_project>/docker-repo/mcp-server-flight-booking
docker push us-central1-docker.pkg.dev/<replace_project>/docker-repo/mcp-server-flight-booking

gcloud run deploy mcp-server-flight-booking-service \
--region us-central1 \
--port=8080 \
--no-allow-unauthenticated \
--image us-central1-docker.pkg.dev/<replace_project>/docker-repo/mcp-server-flight-booking
```

# Test the MCP server
Use the `mcp_client/mcp_client_sse.py` by uncommenting the portions of code to test the MCP server utility.

# Deploy the MCP Agent
```
cd ~/adk-examples/ai-adk-mcp-cloud-run-flightbooking/mcp_agent/

gcloud run deploy adk-mcp-agent-service \
--source . \
--region us-central1 \
--project <Initiate> \
--allow-unauthenticated \
--set-env-vars="GOOGLE_CLOUD_PROJECT=<Initiate>,GOOGLE_CLOUD_LOCATION=<Initiate>,GOOGLE_GENAI_USE_VERTEXAI=True,MCP_SERVER_URL=<Initiate MCP server URL>
```