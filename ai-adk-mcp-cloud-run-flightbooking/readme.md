# Table Creation
create or replace table `<replace_project>.flight_ds.flight_bookings`
(
  user_id string,
  booking_id string,
  from_location string,
  to_location string,
  flight_date datetime,
  booking_status string
);

# Server Execution 
python main.py


# Build the Docker Image to deploy to Cloud Run
gcloud auth configure-docker us-central1-docker.pkg.dev
docker build . -t us-central1-docker.pkg.dev/<replace_project>/docker-repo/mcp-server-flight-booking
docker push us-central1-docker.pkg.dev/<replace_project>/docker-repo/mcp-server-flight-booking

gcloud run deploy mcp-server-flight-booking-service --region us-central1 \
--port=8080 \
--no-allow-unauthenticated \
--image us-central1-docker.pkg.dev/<replace_project>/docker-repo/mcp-server-flight-booking

