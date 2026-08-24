import requests
from datetime import datetime

def fetch_github_user_data(username):
    """Fetches public repositories for a GitHub user and calculates metrics."""
    
    url = f"https://api.github.com/users/{username}/repos"
    
    # Optional but good practice: Add a User-Agent header
    headers = {"User-Agent": "Python-CLI-Analyzer"}
    
    print(f"Fetching data for GitHub user: '{username}'...\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=40)
        
        # Handle 404 errors if the user doesn't exist
        if response.status_code == 404:
            print(f"Error: GitHub user '{username}' not found.")
            return
            
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print(f"Network Error: Could not fetch data. Details: {e}")
        return

    # 1. Parse JSON response into a list of dictionaries
    repos = response.json()
    
    if not repos:
        print(f"User '{username}' has no public repositories.")
        return

    # 2. Initialize variables for metric calculations
    total_stars = 0
    total_size = 0
    max_stars = -1
    max_starred_repo = ""
    most_recent_date = None
    most_recent_repo = ""

    # 3. Iterate through repositories to gather metrics
    for repo in repos:
        stars = repo.get("stargazers_count", 0)
        size = repo.get("size", 0) # Size is in KB
        
        # Datetime parsing: GitHub returns dates in ISO 8601 format (e.g., "2023-10-25T14:30:00Z")
        pushed_at_str = repo.get("pushed_at")
        if pushed_at_str:
            pushed_at_date = datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ")
            
            # Find the most recently updated repo
            if most_recent_date is None or pushed_at_date > most_recent_date:
                most_recent_date = pushed_at_date
                most_recent_repo = repo.get("name")

        # Aggregate totals
        total_stars += stars
        total_size += size

        # Find max stars
        if stars > max_stars:
            max_stars = stars
            max_starred_repo = repo.get("name")

    # 4. Calculate final metrics (Averages)
    repo_count = len(repos)
    avg_stars = total_stars / repo_count
    avg_size_kb = total_size / repo_count

    # 5. Display a clean CLI output
    print("-" * 40)
    print(f"📊 GITHUB REPOSITORY ANALYTICS FOR '{username.upper()}'")
    print("-" * 40)
    print(f"Total Public Repos : {repo_count}")
    print(f"Total Stars        : {total_stars}")
    print(f"Average Stars      : {avg_stars:.2f} per repo")
    print(f"Average Repo Size  : {avg_size_kb:.2f} KB")
    print("-" * 40)
    
    if max_stars > 0:
        print(f"🌟 Most Popular Repo: {max_starred_repo} ({max_stars} stars)")
    else:
        print("🌟 Most Popular Repo: None (No stars yet!)")
        
    if most_recent_date:
        # Format the datetime object back into a clean string
        formatted_date = most_recent_date.strftime("%B %d, %Y at %I:%M %p")
        print(f"🕒 Most Recent Push : {most_recent_repo} (on {formatted_date})")
    print("-" * 40)

if __name__ == "__main__":
    # You can change this to any valid GitHub username
    target_username = input("Enter a GitHub username to analyze: ").strip()
    
    if target_username:
        fetch_github_user_data(target_username)
    else:
        print("Username cannot be empty. Exiting.")