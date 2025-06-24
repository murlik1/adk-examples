# Data Setup
Run setup.sql in bigquery console

# Cloning the repository
cd ~
git clone https://github.com/murlik1/adk-examples.git

# Virtual Environment Setup
cd ~ 
python -m pip install virtualenv --break-system-packages
python -m virtualenv venv 
source ./venv/bin/activate
python -m pip install -r ~/adk-examples/ai-adk-nl2sql/requirements.txt

# Perform configuration changes
nl2sql/.env file to initiate the environment variables

# Local Execution
cd ~/adk-examples/ai-adk-nl2sql/
adk web

# Deploy to Cloud Run
gcloud run deploy adk-nl2sql-service \
--source . \
--region us-central1 \
--project <Initiate> \
--allow-unauthenticated \
--set-env-vars="GOOGLE_CLOUD_PROJECT=<Initiate>,GOOGLE_CLOUD_LOCATION=<Initiate>,GOOGLE_GENAI_USE_VERTEXAI=True"