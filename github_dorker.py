import requests
import os

# Load GitHub Token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ ERROR: GitHub Token not found. Please set it using 'export GITHUB_TOKEN=your_token'")
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

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Run dorks for each organization
for org in orgs:
    print(f"\n🔍 Searching in organization: {org}\n" + "-" * 50)
    
    for dork in dorks:
        url = f"https://api.github.com/search/code?q={dork}+org:{org}+in:file"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json()
            total_count = results.get("total_count", 0)

            if total_count > 0:
                print(f"\n✅ Found {total_count} results for {dork} in {org}:")
                for item in results.get("items", []):
                    repo_name = item["repository"]["full_name"]
                    file_url = item["html_url"]
                    print(f"📂 {repo_name} → 🔗 {file_url}")

        else:
            print(f"❌ Failed to search {dork} in {org}, Status Code: {response.status_code}")

print("\n🎯 GitHub Dorking Complete! Review your results.")
