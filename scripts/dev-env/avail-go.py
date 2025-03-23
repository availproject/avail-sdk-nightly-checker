import os
import re
import subprocess
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the desktop directory
load_dotenv("/root/desktop/.env")

# Target directory for the new avail-go environment
TARGET_DIR = "/root/desktop/avail-go"
# URL for the markdown documentation
DOCS_URL = "https://raw.githubusercontent.com/availproject/docs/refs/heads/main/app/api-reference/avail-node-api/page.mdx"

def fetch_markdown():
    """Fetch the markdown content from the URL"""
    print(f"Fetching markdown from {DOCS_URL}")
    response = requests.get(DOCS_URL)
    if response.status_code != 200:
        print(f"Error fetching markdown: {response.status_code}")
        sys.exit(1)
    return response.text

def extract_command(markdown, cmd_name):
    """Extract a specific terminal command from markdown by name"""
    pattern = f'```bash filename="terminal" name="{cmd_name}"\\s+(.*?)\\s+```'
    match = re.search(pattern, markdown, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_content(markdown, content_name):
    """Extract content from markdown by name - works for any type of code block"""
    pattern = f'```.*?name="{content_name}"\\s+(.*?)\\s+```'
    match = re.search(pattern, markdown, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def create_directory():
    """Create the target directory if it doesn't exist, or delete and recreate it if it does"""
    if os.path.exists(TARGET_DIR):
        print(f"Target directory {TARGET_DIR} already exists. Removing it...")
        try:
            import shutil
            shutil.rmtree(TARGET_DIR)
            print(f"Successfully removed existing directory: {TARGET_DIR}")
        except Exception as e:
            print(f"Error removing existing directory: {e}")
            sys.exit(1)
    
    # Create the directory (either it didn't exist or we just deleted it)
    try:
        os.makedirs(TARGET_DIR)
        print(f"Created directory: {TARGET_DIR}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        sys.exit(1)

def run_command(command):
    """Run the command in the target directory, handling && operators"""
    print(f"Running command: {command}")
    
    # Check if the command contains &&
    if "&&" in command:
        # Split the command by && and strip whitespace
        sub_commands = [cmd.strip() for cmd in command.split("&&")]
        print(f"Detected compound command with {len(sub_commands)} parts")
        
        # Run each sub-command in sequence
        for i, sub_cmd in enumerate(sub_commands):
            print(f"Running part {i+1}/{len(sub_commands)}: {sub_cmd}")
            success = run_command(sub_cmd)  # Recursive call for each part
            if not success:
                print(f"Part {i+1} failed, stopping compound command")
                return False
        return True  # All parts succeeded
    
    # For simple commands without &&, use the original logic
    try:
        # Split command into args for subprocess
        cmd_args = command.split()
        result = subprocess.run(cmd_args, cwd=TARGET_DIR, capture_output=True, text=True)
        print(f"Command output: {result.stdout}")
        if result.stderr:
            print(f"Error output: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error executing command: {e}")
        return False

def write_env_file(content):
    """Write content to .env file with the specified seed phrase"""
    env_path = os.path.join(TARGET_DIR, ".env")
    
    # Get seed phrase from environment variables
    seed_phrase = os.environ.get("SEED")
    if not seed_phrase:
        print("Error: SEED environment variable not found or empty")
        print("Please set a valid SEED in your .env file")
        sys.exit(1)
    
    # Replace the placeholder seed phrase with the actual one
    updated_content = content.replace(
        "This is a random seed phrase please replace with your own",
        seed_phrase
    )
    
    # Write the content to the file
    try:
        with open(env_path, 'w') as f:
            f.write(updated_content)
        print(f"Successfully wrote environment variables to {env_path}")
        return True
    except Exception as e:
        print(f"Error writing to .env file: {e}")
        sys.exit(1)

def main():
    # Create the target directory
    create_directory()
    
    # Fetch markdown content
    markdown = fetch_markdown()

    # Extract command cmd14 - Go mod init
    cmd14 = extract_command(markdown, "cmd14")
    if cmd14:
        print(f"Found command cmd14: {cmd14}")
        # Replace project name with our directory name
        cmd14 = cmd14.replace("your-project-name", "avail-go")
        success = run_command(cmd14)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)
    else:
        print("Command cmd14 not found in markdown")
        sys.exit(1)

    # Extract command cmd15 - Install avail-go-sdk
    cmd15 = extract_command(markdown, "cmd15")
    if cmd15:
        print(f"Found command cmd15: {cmd15}")
        success = run_command(cmd15)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)
    else:
        print("Command cmd15 not found in markdown")
        sys.exit(1)

    # Extract command cmd16 - Install godotenv
    cmd16 = extract_command(markdown, "cmd16")
    if cmd16:
        print(f"Found command cmd16: {cmd16}")
        success = run_command(cmd16)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)
    else:
        print("Command cmd16 not found in markdown")
        sys.exit(1)

    # Extract command cmd17 - Create .env file
    cmd17 = extract_command(markdown, "cmd17")
    if cmd17:
        print(f"Found command cmd17: {cmd17}")
        success = run_command(cmd17)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)
    else:
        print("Command cmd17 not found in markdown")
        sys.exit(1)

    # Extract content cmd18 - Write to .env file
    env_content = extract_content(markdown, "cmd18")
    if env_content:
        print("Found .env content")
        success = write_env_file(env_content)
    else:
        print(".env content not found in markdown")
        sys.exit(1)

    # Create empty main.go file
    main_go_path = os.path.join(TARGET_DIR, "main.go")
    try:
        with open(main_go_path, 'w') as f:
            f.write("")  # Write an empty file
        print(f"Created empty main.go file at {main_go_path}")
    except Exception as e:
        print(f"Error creating main.go file: {e}")
        sys.exit(1)

    print("Go development environment setup completed successfully!")

if __name__ == "__main__":
    main()
