#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the desktop directory
load_dotenv("/root/desktop/.env")

# Target directory for the new avail-js environment
TARGET_DIR = "/root/desktop/avail-js"
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
    # Pattern matches any code block with name="cmd6" regardless of language
    pattern = f'```.*?name="{content_name}"\\s+(.*?)\\s+```'
    match = re.search(pattern, markdown, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def write_tsconfig(content):
    """Write content to tsconfig.json file"""
    tsconfig_path = os.path.join(TARGET_DIR, "tsconfig.json")
    
    # Check if the file exists
    if not os.path.exists(tsconfig_path):
        print(f"Error: tsconfig.json does not exist at {tsconfig_path}")
        sys.exit(1)
        
    # Write the content to the file
    try:
        with open(tsconfig_path, 'w') as f:
            f.write(content)
        print(f"Successfully wrote configuration to {tsconfig_path}")
        return True
    except Exception as e:
        print(f"Error writing to tsconfig.json: {e}")
        sys.exit(1)

def write_env_file(content):
    """Write content to .env file with the specified seed phrase"""
    env_path = os.path.join(TARGET_DIR, ".env")
    
    # Check if the file exists
    if not os.path.exists(env_path):
        print(f"Error: .env file does not exist at {env_path}")
        sys.exit(1)
    
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

def main():
    # Create the directory
    create_directory()
    
    # Fetch markdown content
    markdown = fetch_markdown()
    
    # Extract command cmd2
    # Run `pnpm init to initialize the JS project`
    cmd2 = extract_command(markdown, "cmd2")
    if cmd2:
        print(f"Found command cmd2: {cmd2}")
        success = run_command(cmd2)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)  # Exit if command execution failed
    else:
        print("Command cmd2 not found in markdown")
        sys.exit(1)  # Exit if command not found

    # Extract command cmd3
    # Run `pnpm add avail-js-sdk@0.4.0` to install the avail-js-sdk
    cmd3 = extract_command(markdown, "cmd3")
    if cmd3:
        print(f"Found command cmd3: {cmd3}")
        success = run_command(cmd3)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)  # Exit if command execution failed
    else:
        print("Command cmd3 not found in markdown")
        sys.exit(1)  # Exit if command not found


    # Extract command cmd5
    # Run `touch tsconfig.json` to create the tsconfig.json file
    cmd5 = extract_command(markdown, "cmd5")
    if cmd5:
        print(f"Found command cmd5: {cmd5}")
        success = run_command(cmd5)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)  # Exit if command execution failed
    else:
        print("Command cmd5 not found in markdown")
        sys.exit(1)  # Exit if command not found
    
    # Extract content cmd6
    # Extract tsconfig.json content and write to file
    tsconfig_content = extract_content(markdown, "cmd6")
    if tsconfig_content:
        print("Found tsconfig.json content")
        success = write_tsconfig(tsconfig_content)
    else:
        print("tsconfig.json content not found in markdown")
        sys.exit(1)

    # Extract command cmd7
    # run `pnpm add dotenv && touch .env` to install dotenv and create .env file
    cmd7 = extract_command(markdown, "cmd7")
    if cmd7:
        print(f"Found command cmd7: {cmd7}")
        success = run_command(cmd7)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)  # Exit if command execution failed
    else:
        print("Command cmd7 not found in markdown")
        sys.exit(1)  # Exit if command not found

    # Extract content cmd8
    # Write to .env file
    env_content = extract_content(markdown, "cmd8")
    if env_content:
        print("Found .env content")
        success = write_env_file(env_content)
    else:
        print(".env content not found in markdown")
        sys.exit(1)

    # Create a TypeScript file if it doesn't exist
    ts_file_path = os.path.join(TARGET_DIR, "your-file-name.ts")
    if not os.path.exists(ts_file_path):
        try:
            with open(ts_file_path, 'w') as f:
                f.write('// Empty TypeScript file for Avail JS SDK examples\n')
            print(f"Successfully created file: {ts_file_path}")
        except Exception as e:
            print(f"Error creating TypeScript file: {e}")
            sys.exit(1)
    else:
        print(f"File already exists: {ts_file_path}")

    print("Avail JS development environment setup completed successfully!")

if __name__ == "__main__":
    main()