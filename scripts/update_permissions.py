import yaml
import requests
import os

# Load GitHub token from environment variables
GITHUB_TOKEN = os.getenv("GH_PAT")  # Changed to use the correct secret name
GITHUB_API_URL = "https://api.github.com"

# Read members_permissions.yml
def load_permissions():
    with open("config/members_permissions.yml", "r") as file:
        return yaml.safe_load(file)

# Assign users to teams and repositories
def update_permissions():
    data = load_permissions()
    
    for org, details in data["organisations"].items():
        for team, info in details["teams"].items():
            for user in info["members"]:
                add_user_to_team(org, team, user)
            for repo, permission in info["repositories"].items():
                set_repo_permission(org, team, repo, permission)

# Add user to GitHub Team
def add_user_to_team(org, team, user):
    url = f"{GITHUB_API_URL}/orgs/{org}/teams/{team}/memberships/{user}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.put(url, headers=headers, json={"role": "member"})
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ Successfully added {user} to {team}")
    else:
        print(f"❌ Failed to add {user} to {team}: {response.status_code} - {response.text}")

# Set repository permissions for team
def set_repo_permission(org, team, repo, permission):
    url = f"{GITHUB_API_URL}/orgs/{org}/teams/{team}/repos/{org}/{repo}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.put(url, headers=headers, json={"permission": permission})
    if response.status_code == 200 or response.status_code == 201:
        print(f"✅ Set {permission} permission for {team} on {repo}")
    else:
        print(f"❌ Failed to set permission for {team} on {repo}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    update_permissions()
