# Python Packages setup
```
cd ~ 
python -m pip install virtualenv --break-system-packages
python -m virtualenv venv 
source ./venv/bin/activate
python -m pip install -r ~/adk-examples/ai-adk-mcp-cloud-run-flightbooking/mcp_server/requirements.txt
```

# Table Creation
```
create schema `<replace_project>.flight_demo_ds`;
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

# Create artifact registry in `us-central1` with name `cloud-run-source-deploy` of `docker` type

# Deploy MCP Server to Cloud Run
```
cd ~/adk-examples/ai-adk-mcp-cloud-run-flightbooking/mcp_server 

docker build . -t  us-central1-docker.pkg.dev/<project>/cloud-run-source-deploy/mcp-server-flight-booking
docker push us-central1-docker.pkg.dev/<project>/cloud-run-source-deploy/mcp-server-flight-booking

Local Deployment
#####################
docker run -it \
-e PROJECT=<Initiate> \
-e DATASET=flight_demo_ds \
-e TABLE=flight_bookings \
-e PORT=8080 \
-p 8080:8080 \
us-central1-docker.pkg.dev/adk-integration-mcp-1326/cloud-run-source-deploy/mcp-server-flight-booking

gcloud run deploy mcp-server-flight-booking-service \
--image us-central1-docker.pkg.dev/<project>/cloud-run-source-deploy/mcp-server-flight-booking \
--project <project> \
--region us-central1 \
--port=8080 \
--no-allow-unauthenticated \
--set-env-vars="PROJECT=<project>,DATASET=flight_demo_ds,TABLE=flight_bookings"
```

# Test the MCP server
## Initiate the MCP Server Cloud Run URL in the MCP Client
Use the `mcp_client/mcp_client_sse.py` by uncommenting the portions of code to test the MCP server utility.

```
cd ~/adk-examples/ai-adk-mcp-cloud-run-flightbooking/mcp_client
python mcp_client_sse.py
```

# Deploy the MCP Agent
```
cd ~/adk-examples/ai-adk-mcp-cloud-run-flightbooking/mcp_agent/

docker build . -t  us-central1-docker.pkg.dev/<Initiate>/cloud-run-source-deploy/mcp-agent-service

docker run -it \
-e PORT=8080 \
-p 8080:8080 \
us-central1-docker.pkg.dev/<Initiate>/cloud-run-source-deploy/mcp-agent-service

docker push us-central1-docker.pkg.dev/<Initiate>/cloud-run-source-deploy/mcp-agent-service

gcloud run deploy adk-mcp-agent-service \
--image us-central1-docker.pkg.dev/<Initiate>/cloud-run-source-deploy/mcp-agent-service \
--region us-central1 \
--project <Initiate> \
--allow-unauthenticated \
--set-env-vars="GOOGLE_CLOUD_PROJECT=<Initiate>,GOOGLE_CLOUD_LOCATION=<Initiate>,GOOGLE_GENAI_USE_VERTEXAI=True,MCP_SERVER_URL=<Initiate MCP server URL>
```