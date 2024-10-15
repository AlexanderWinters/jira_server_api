# Jira Server API (WIP)
Function for the Jira Server API.

This is a python script that contains function for the Jira API:
- Bulk adding users and sending emails
- Bulk creating projects
- Getting project category IDs

Edit the SERVER environmental variable to match your server domain (not URL). The script default to the http protocol (will add functionality for https).
To bulk create projects:
- Run the script to get all the project category IDs.
- Find your project category and then it's ID.
- Edit the CATEGORY_ID variable and add the key for your category.
- Edit the PROJECT_KEY. Needs to be short.
- Edit the PROJECT_PREFIX. the prefix to the group name, as project name.

