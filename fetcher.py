import requests
from datetime import datetime

def fetch_github_user_data(username):
    
    url = f"https://api.github.com/users/{username}/repos"
    
    headers = {"User-Agent": "Python-CLI-Analyzer"}
    
    print(f"Fetching data for GitHub user: '{username}'...\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=40)
        

        if response.status_code == 404:
            print(f"Error: GitHub user '{username}' not found.")
            return
            
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print(f"Network Error: Could not fetch data. Details: {e}")
        return

    # Parsing JSON 
    repos = response.json()
    
    if not repos:
        print(f"User '{username}' has no public repositories.")
        return

    # Initialize variables 
    total_stars = 0
    total_size = 0
    max_stars = -1
    max_starred_repo = ""
    most_recent_date = None
    most_recent_repo = ""

    # Iterate through repos
    for repo in repos:
        stars = repo.get("stargazers_count", 0)
        size = repo.get("size", 0) # Size is in KB
        
        # parsing in ISO 8601 format
        pushed_at_str = repo.get("pushed_at")
        if pushed_at_str:
            pushed_at_date = datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ")
        
            if most_recent_date is None or pushed_at_date > most_recent_date:
                most_recent_date = pushed_at_date
                most_recent_repo = repo.get("name")

        
        total_stars += stars
        total_size += size
        
        if stars > max_stars:
            max_stars = stars
            max_starred_repo = repo.get("name")

    # final metrics
    repo_count = len(repos)
    avg_stars = total_stars / repo_count
    avg_size_kb = total_size / repo_count

    # For clean  output
    print("-" * 40)
    print(f" GITHUB REPOSITORY ANALYTICS FOR '{username.upper()}'")
    print("-" * 40)
    print(f"Total Public Repos : {repo_count}")
    print(f"Total Stars        : {total_stars}")
    print(f"Average Stars      : {avg_stars:.2f} per repo")
    print(f"Average Repo Size  : {avg_size_kb:.2f} KB")
    print("-" * 40)
    
    if max_stars > 0:
        print(f"Most Popular Repo: {max_starred_repo} ({max_stars} stars)")
    else:
        print("Most Popular Repo: None (No stars yet!)")
        
    if most_recent_date:
        # Formating datetime 
        formatted_date = most_recent_date.strftime("%B %d, %Y at %I:%M %p")
        print(f" Most Recent Push : {most_recent_repo} (on {formatted_date})")
    print("-" * 40)

if __name__ == "__main__":
    
    target_username = input("Enter a GitHub username to analyze: ").strip()
    
    if target_username:
        fetch_github_user_data(target_username)
    else:
        print("Username cannot be empty. Exiting.")
