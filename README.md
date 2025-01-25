# Jira API Toolbox
Jira sucks, so I made an API toolbox. A Streamlit web app that interacts with the Jira API. 
<img width="997" alt="Screenshot 2025-01-25 at 20 59 34" src="https://github.com/user-attachments/assets/3d78ac9d-b11f-4c9c-b46c-563d94df8d41" />


## Deploy locally
Install the Docker engine and run the following:
```
docker run -p 3000:8501 alexanderwinters/jira_api:latest
```
You can also download the docker compose file and run:
```
curl -o docker-compose.yml https://raw.githubusercontent.com/AlexanderWinters/jira_server_api/refs/heads/main/docker-compose.yml
docker compose up -d
```

## Local Development
Clone the repo and install the ```requirements.txt```:
```
git clone https://github.com/AlexanderWinters/jira_server_api.git
cd jira_server_api
pip3 install -r requirements.txt
```
This will install streamlit as well. You can then test run it:
```
streamlit run app.py
```
## Future goals
- [ ] Expand API functions
- [ ] The API is based on Jira 8.14, although it has remained pretty similar. Investigate
- [ ] Mobile app
- [ ] Make a public instance
