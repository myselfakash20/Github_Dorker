import requests
import os
import time

# Load GitHub Token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("❌ ERROR: GitHub Token not found. Set it using 'export GITHUB_TOKEN=your_token'")
    exit()

# Ask the user for organization(s) input
orgs_input = input("Enter GitHub organization(s) (for multiple, separate by commas): ").strip()
orgs = [org.strip() for org in orgs_input.split(",")]

# List of advanced GitHub dorks
dorks = [
    "AWS_SECRET_ACCESS_KEY", "AZURE_SUBSCRIPTION_ID", "GOOGLE_APPLICATION_CREDENTIALS",
    "DOCKER_AUTH_CONFIG", "JENKINS_API_TOKEN", "PAYPAL_LIVE_API_USERNAME", "STRIPE_SECRET_KEY",
    "MONGO_INITDB_ROOT_PASSWORD", "POSTGRES_PASSWORD", "SMTP_PASSWORD", "SLACK_API_TOKEN",
    "DISCORD_BOT_TOKEN", "TWILIO_ACCOUNT_SID", "FIREBASE_API_KEY", "filename:.npmrc",
    "filename:.env", "filename:database.yml", "filename:wp-config.php", "filename:.git-credentials",
    "filename:.bash_history", "filename:.kube/config", "filename:elasticsearch.yml",
    "filename:mongo.conf", "filename:redis.conf", "filename:oauth.json", "filename:authorized_keys"
]

# Set headers for GitHub API requests
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Check API rate limits
def check_rate_limit():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rate_limit_data = response.json()
        remaining_requests = rate_limit_data["rate"]["remaining"]
        reset_time = rate_limit_data["rate"]["reset"]
        return remaining_requests, reset_time
    else:
        return 0, 0  # If API call fails, assume limit reached

# Function to handle API rate limits and retries
def make_request(url):
    while True:
        remaining_requests, reset_time = check_rate_limit()
        
        if remaining_requests == 0:
            wait_time = max(reset_time - time.time(), 60)  # Wait at least 60 seconds
            print(f"⚠️ Rate limit reached. Waiting {int(wait_time)} seconds...")
            time.sleep(wait_time)

        response = requests.get(url, headers=headers)

        if response.status_code == 403:
            print("⚠️ API rate limit hit. Retrying in 60 seconds...")
            time.sleep(60)
        elif response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed request: Status Code {response.status_code}")
            return None

# Run dorks for each organization
for org in orgs:
    print(f"\n🔍 Searching in organization: {org}\n" + "-" * 50)
    
    for dork in dorks:
        url = f"https://api.github.com/search/code?q={dork}+org:{org}+in:file"
        results = make_request(url)

        if results and results.get("total_count", 0) > 0:
            print(f"\n✅ Found {results['total_count']} results for {dork} in {org}:")
            for item in results.get("items", []):
                repo_name = item["repository"]["full_name"]
                file_url = item["html_url"]
                print(f"📂 {repo_name} → 🔗 {file_url}")

print("\n🎯 GitHub Dorking Complete! Review your results.")
