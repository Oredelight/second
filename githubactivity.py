import sys
import urllib.request
import json
from datetime import datetime, timezone

GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
GRAY = "\033[90m"
RESET = "\033[0m"

def time_ago(event_time):
    event_datetime = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%SZ")
    event_datetime = event_datetime.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = now - event_datetime

    seconds = diff.total_seconds()
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"

def getUsername(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
       response= urllib.request.urlopen(url)
       data= response.read().decode("utf-8")
       events = json.loads(data)

       if not events:
           print(f"{YELLOW}No recent activity found for {username}.{RESET}")
           return

       for event in events[:10]:
           event_type= event["type"]
           repo_name= event["repo"]["name"]
           created_at= event["created_at"]
           ago= time_ago(created_at)

           if event_type == "PushEvent":
               commits= event["payload"].get("size", 0)
               print(f"{GREEN} Pushed {commits} commit{'s' if commits > 1 else ''} to {repo_name} ({ago}){RESET}")
           elif event_type == "CreateEvent":
                ref_type= event["payload"].get("ref_type", "repository")
                print(f"{BLUE} Created a new {ref_type} in {repo_name} ({ago}){RESET}")
           elif event_type == "IssuesEvent":
                action = event["payload"]["action"]
                print(f"{YELLOW} {action.capitalize()} an isssue in {repo_name} ({ago}){RESET}")
           elif event_type == "WatchEvent":
                print(f"{MAGENTA} Starred {repo_name} ({ago}){RESET}")
           elif event_type == "ForkEvent":
                print(f"{CYAN} Forked {repo_name} ({ago}){RESET}")
       else:
            print(f"{GRAY} {event_type} in {repo_name} ({ago}){RESET}")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"{YELLOW}User '{username}' not found.{RESET}")
        else:
            print(f"{YELLOW}HTTP Error {e.code}: Could not fetch data.{RESET}")

    except Exception as e:
        print(f"{YELLOW}An error occurred: {e}{RESET}")

def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter your username: ").strip()
   
    getUsername(username)

if __name__ == "__main__":
    main()