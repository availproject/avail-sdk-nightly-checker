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
TARGET_DIR = "/root/desktop/avail-rust"
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

def write_cargo_toml(content):
    """Write content to Cargo.toml file"""
    cargo_path = os.path.join(TARGET_DIR, "Cargo.toml")
    
    # Check if the file exists
    if not os.path.exists(cargo_path):
        print(f"Error: Cargo.toml does not exist at {cargo_path}")
        sys.exit(1)
        
    # Write the content to the file
    try:
        with open(cargo_path, 'w') as f:
            f.write(content)
        print(f"Successfully wrote configuration to {cargo_path}")
        return True
    except Exception as e:
        print(f"Error writing to Cargo.toml: {e}")
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

    # Extract command cmd9
    # To initialize the rust project
    cmd9 = extract_command(markdown, "cmd9")
    if cmd9:
        print(f"Found command cmd9: {cmd9}")
        success = run_command(cmd9)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)  # Exit if command execution failed
    else:
        print("Command cmd9 not found in markdown")
        sys.exit(1)  # Exit if command not found

    # Extract content cmd10
    # Extract Cargo.toml content and write to file
    cargo_content = extract_content(markdown, "cmd10")
    if cargo_content:
        print("Found Cargo.toml content")
        # Update the project name to match our directory name
        cargo_content = cargo_content.replace("your-project-name", "avail-rust")
        success = write_cargo_toml(cargo_content)
    else:
        print("Cargo.toml content not found in markdown")
        sys.exit(1)
        
    # Extract command cmd11
    # Run `touch .env` to create the .env file
    cmd11 = extract_command(markdown, "cmd11")
    if cmd11:
        print(f"Found command cmd11: {cmd11}")
        success = run_command(cmd11)
        print(f"Command execution {'succeeded' if success else 'failed'}")
        if not success:
            sys.exit(1)  # Exit if command execution failed
    else:
        print("Command cmd11 not found in markdown")
        sys.exit(1)  # Exit if command not found

    # Extract content cmd12
    # Write to .env file
    env_content = extract_content(markdown, "cmd12")
    if env_content:
        print("Found .env content")
        success = write_env_file(env_content)
    else:
        print(".env content not found in markdown")
        sys.exit(1)    
    # Add cargo build with timeout to pre-compile dependencies
    print("\n=== Pre-compiling Rust dependencies (this may take several minutes) ===")
    try:
        # Use subprocess directly for this long-running command to set a longer timeout
        result = subprocess.run(
            ["cargo", "build"], 
            cwd=TARGET_DIR, 
            capture_output=True, 
            text=True,
            timeout=900  # 15 minutes timeout
        )
        
        print("Cargo build output:")
        print(result.stdout)
        
        if result.stderr:
            print("Cargo build stderr:")
            print(result.stderr)
            
        if result.returncode != 0:
            print(f"Cargo build failed with return code {result.returncode}")
            sys.exit(1)
        else:
            print("Cargo build completed successfully")
            
    except subprocess.TimeoutExpired:
        print("Cargo build timed out after 900 seconds")
        sys.exit(1)
    except Exception as e:
        print(f"Error during cargo build: {e}")
        sys.exit(1)

    print("Rust development environment setup completed successfully!")

if __name__ == "__main__":
    main()