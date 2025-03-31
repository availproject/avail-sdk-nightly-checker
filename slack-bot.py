import json
import datetime
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define path to results file
RESULTS_FILE = "run-results.json"

# Read results from JSON file
def read_results():
    try:
        with open(RESULTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {RESULTS_FILE} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not parse {RESULTS_FILE}")
        return None

# --- Slack Integration: Post results from JSON file ---
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=SLACK_BOT_TOKEN)

# Get results from JSON file
data = read_results()
if not data:
    print("Failed to read results data. Exiting.")
    exit(1)

# Extract timestamp and results
timestamp = data.get("last_run_timestamp", "Unknown time")
results = data.get("results", {})

# Format the timestamp for display
try:
    dt = datetime.datetime.fromisoformat(timestamp)
    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    formatted_date = dt.strftime("%Y-%m-%d")  # Just the date portion for the mention
except (ValueError, TypeError):
    formatted_time = timestamp
    formatted_date = "today"  # Fallback if we can't parse the timestamp

# Build a message string with a mention and date before the code block
message = f"<@U0689CNJQEA>, these are the results for the nightly run for {formatted_date}:\n\n"
message += f"• The full log file can be found at <https://github.com/availproject/avail-sdk-nightly-checker/blob/main/last-run-log.txt|last-run-log.txt>\n"
message += f"• The JSON formatted results can be found at <https://github.com/availproject/avail-sdk-nightly-checker/blob/main/run-results.json|run-results.json>\n\n"
message += f"*Avail SDK Tests - Run at {formatted_time}*\n```\n"

# Use enumerate to get both index and item
for i, (label, value) in enumerate(results.items(), 1):  # Start counting from 1
    status = "✅" if value else "❌"
    # Format the label more nicely by replacing underscores with spaces and capitalizing
    display_label = label.replace("_", " ").title()
    message += f"{i}. {display_label}: {status}\n"  # Add the number with a period
message += "```"

try:
    response = client.chat_postMessage(
        channel="#avail-node-sdks-nightly-check",  # Replace with your channel name
        text=message,
        unfurl_links=False,
        unfurl_media=False
    )
    print("Message posted successfully:", response["ts"])
except SlackApiError as e:
    print(f"Error posting message: {e.response['error']}")