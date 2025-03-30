#!/usr/bin/env python
import subprocess
import re
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set current working directory to script location to ensure consistent paths
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Path to results file
RESULTS_FILE = "/root/desktop/run-results.json"
LOG_FILE = "/root/desktop/last-run-log.txt"

# Create a custom output capturer
class OutputCapturer:
    def __init__(self):
        self.terminal = sys.stdout
        self.log_content = []
    
    def write(self, message):
        self.terminal.write(message)
        self.log_content.append(message)
    
    def flush(self):
        self.terminal.flush()
    
    def get_content(self):
        return ''.join(self.log_content)

# Clear log file at beginning
with open(LOG_FILE, 'w') as f:
    f.write("")  # Empty the file
print(f"Cleared log file: {LOG_FILE}")

# Set up output capture
output_capturer = OutputCapturer()
sys.stdout = output_capturer

# Reset all results to false at the beginning of each run
def reset_results():
    print("\n=== Resetting all test results to false ===")
    
    # Create default structure if file doesn't exist
    if not os.path.exists(RESULTS_FILE):
        default_results = {
            "last_run_timestamp": "",
            "results": {
            }
        }
        with open(RESULTS_FILE, 'w') as f:
            json.dump(default_results, f, indent=2)
        print(f"Created new results file at {RESULTS_FILE}")
        return
    
    try:
        # Read existing file
        with open(RESULTS_FILE, 'r') as f:
            results_data = json.load(f)
        
        # Reset all values to false
        for key in results_data.get("results", {}):
            results_data["results"][key] = False
        
        # Update timestamp
        results_data["last_run_timestamp"] = datetime.now().isoformat()
        
        # Write back to file
        with open(RESULTS_FILE, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print("Successfully reset all test results to false")
    except Exception as e:
        print(f"Error resetting results: {e}")

# Reset all results to false
reset_results()

def push_to_github():
    """Push results and logs to GitHub repository"""
    print("\n=== Pushing results to Git repository ===")
    try:
        # Get current timestamp for commit message
        current_time = datetime.now().isoformat()
        
        # Get GitHub token from environment (loaded from .env)
        github_token = os.environ.get("GITHUB_TOKEN")
        if not github_token:
            print("Error: GITHUB_TOKEN not found in environment variables")
            print("Please ensure GITHUB_TOKEN is set in your .env file")
            return False
        
        # Get email for Git identity
        email = os.environ.get("EMAIL")
        if not email:
            print("Error: EMAIL not found in environment variables")
            print("Please ensure EMAIL is set in your .env file")
            return False
        
        # Stage changes
        print("\nStaging changes...")
        stage_result = subprocess.run(
            ["git", "add", "run-results.json", "last-run-log.txt"],
            cwd="/root/desktop",
            capture_output=True,
            text=True
        )
        if stage_result.returncode != 0:
            print(f"Failed to stage files: {stage_result.stderr.strip()}")
            return False
        
        # Check if there are changes to commit
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd="/root/desktop",
            capture_output=True,
            text=True
        )
        
        if not status_result.stdout.strip():
            print("No changes to commit")
            return True
        
        # Commit changes with one-time author settings
        print("\nCommitting changes...")
        commit_result = subprocess.run(
            ["git", "-c", "user.name=Avail SDK Nightly Checker", "-c", f"user.email={email}", 
             "commit", "-m", f"Pushing log result of run at {current_time}"],
            cwd="/root/desktop",
            capture_output=True,
            text=True
        )
        if commit_result.returncode != 0:
            print(f"Commit failed: {commit_result.stderr.strip()}")
            return False
        
        # Push changes using token
        print("\nPushing changes to GitHub...")
        repo_url = f"https://{github_token}@github.com/availproject/avail-sdk-nightly-checker.git"
        push_result = subprocess.run(
            ["git", "push", repo_url, "main"],
            cwd="/root/desktop",
            capture_output=True,
            text=True
        )
        
        if push_result.returncode == 0:
            print("Successfully pushed changes to GitHub")
            return True
        else:
            print(f"Push failed: {push_result.stderr.strip()}")
            return False

    except Exception as e:
        print(f"Error during Git operations: {e}")
        return False

try:
    # Force scripts to flush output immediately and add all required paths
    env = os.environ.copy()
    env["PATH"] = "/root/.nvm/versions/node/v22.14.0/bin:/root/.local/share/pnpm:/root/.cargo/bin:/usr/local/go/bin:/usr/bin:/bin:/usr/local/bin:" + env.get("PATH", "")
    env["PYTHONUNBUFFERED"] = "1"

    # Execute the Avail-js environment setup script
    print("\n=== Setting up avail-js environment ===")
    avail_js_env_setup_script = "./scripts/dev-env/avail-js.py"
    print(f"Running script: {os.path.abspath(avail_js_env_setup_script)}")

    try:
        # Use Popen for real-time output streaming
        process = subprocess.Popen(
            ["python", avail_js_env_setup_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
            env=env  # Use the same env with PYTHONUNBUFFERED=1
        )
        
        # Stream output in real-time
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # Print each line as it comes
        
        # Wait for the process to complete and get return code
        return_code = process.wait()
        
        if return_code != 0:
            print(f"\nAvail-js environment setup failed with return code {return_code}")
            sys.exit(1)
        else:
            print("\nAvail-js environment setup completed successfully")
            
    except Exception as e:
        print(f"Error running avail-js environment setup script: {e}")
        sys.exit(1)
    print("\n================================================")


    # Execute the Avail-rust environment setup script
    print("\n=== Setting up avail-rust environment ===")
    avail_rust_env_setup_script = "./scripts/dev-env/avail-rust.py"
    print(f"Running script: {os.path.abspath(avail_rust_env_setup_script)}")

    try:
        # Use Popen for real-time output streaming
        process = subprocess.Popen(
            ["python", avail_rust_env_setup_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
            env=env  # Use the same env with PYTHONUNBUFFERED=1
        )
        
        # Stream output in real-time
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # Print each line as it comes
        
        # Wait for the process to complete and get return code
        return_code = process.wait()
        
        if return_code != 0:
            print(f"\nAvail-rust environment setup failed with return code {return_code}")
            sys.exit(1)
        else:
            print("\nAvail-rust environment setup completed successfully")
            
    except subprocess.TimeoutExpired:
        print(f"Avail-rust environment setup script timed out.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running avail-rust environment setup script: {e}")
        sys.exit(1)
    print("\n================================================")

    # Execute the Avail-go environment setup script
    print("\n=== Setting up avail-go environment ===")
    avail_go_env_setup_script = "./scripts/dev-env/avail-go.py"
    print(f"Running script: {os.path.abspath(avail_go_env_setup_script)}")

    try:
        # Use Popen for real-time output streaming
        process = subprocess.Popen(
            ["python", avail_go_env_setup_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
            env=env  # Use the same env with PYTHONUNBUFFERED=1
        )
        
        # Stream output in real-time
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # Print each line as it comes
        
        # Wait for the process to complete and get return code
        return_code = process.wait()
        
        if return_code != 0:
            print(f"\nAvail-go environment setup failed with return code {return_code}")
            sys.exit(1)
        else:
            print("\nAvail-go environment setup completed successfully")
            
    except subprocess.TimeoutExpired:
        print(f"Avail-go environment setup script timed out.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running avail-go environment setup script: {e}")
        sys.exit(1)
    print("\n================================================")

    # Define a list of script paths and their descriptions
    snippet_scripts = [
        {
            "name": "Data Submission",
            "path": "scripts/snippets/da_submit_data.py"
        },
        {
            "name": "Data Submission from Docs Section",
            "path": "scripts/snippets/da_submit_data_from_docs_section.py"
        },
        {
            "name": "Create Application Key",
            "path": "scripts/snippets/da_create_application_key.py"
        },
        {
            "name": "Balances Transfer Keep Alive",
            "path": "scripts/snippets/balances_transfer_keep_alive.py"
        },
        {
            "name": "Balances Transfer Keep Alive from Docs Section",
            "path": "scripts/snippets/balances_transfer_keep_alive_from_docs_section.py"
        },
        {
            "name": "Balances Transfer Allow Death",
            "path": "scripts/snippets/balances_transfer_allow_death.py"
        },
        {
            "name": "Balances Transfer Allow Death from Docs Section",
            "path": "scripts/snippets/balances_transfer_allow_death_from_docs_section.py"
        },
        {
            "name": "System Account Fetch",
            "path": "scripts/snippets/system_account.py"
        },
        {
            "name": "System Account Fetch from Docs Section",
            "path": "scripts/snippets/system_account_from_docs_section.py"
        },
        {
            "name": "DA Next App ID",
            "path": "scripts/snippets/da_next_app_id.py"
        },
        {
            "name": "DA App Keys",
            "path": "scripts/snippets/da_app_keys.py"
        },
        {
            "name": "DA Submission using txHash and blockHash",
            "path": "scripts/snippets/da_submission_using_txHash_blockHash.py"
        },
        {
            "name": "DA Submission using App ID",
            "path": "scripts/snippets/da_submission_using_appID.py"
        },
        {
            "name": "All DA Submissions for a given block",
            "path": "scripts/snippets/da_all_da_submissions.py"
        },
        {
            "name": "All Transactions by Signer",
            "path": "scripts/snippets/da_all_transactions_by_signer.py"
        },
        {
            "name": "Fetch All Transactions",
            "path": "scripts/snippets/fetch_all_transactions.py"
        }
    ]

    # Execute all snippet scripts in a loop
    for script in snippet_scripts:
        script_name = script["name"]
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script["path"])
        
        print(f"\n=== Running {script_name} script ===")
        print(f"Script path: {script_path}")
        
        try:
            # Use Popen for real-time output streaming
            process = subprocess.Popen(
                ["python", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered
                env=env  # Use the same env with PYTHONUNBUFFERED=1
            )
            
            # Stream output in real-time
            for line in iter(process.stdout.readline, ''):
                print(line, end='')  # Print each line as it comes
            
            # Wait for the process to complete and get return code
            return_code = process.wait()
            print(f"\n{script_name} script completed with return code: {return_code}")
            
            # Optionally handle non-zero return codes
            if return_code != 0:
                print(f"WARNING: {script_name} script returned non-zero exit code: {return_code}")
                # Uncomment if you want to exit on any script failure
                # sys.exit(return_code)
                
        except Exception as e:
            print(f"Error running {script_name} script: {e}")
        
        print("\n================================================")

    # Clean up by removing all SDK directories
    print("\n=== Cleaning up environment directories ===")
    sdk_dirs = [
        "/root/desktop/avail-js",
        "/root/desktop/avail-rust",
        "/root/desktop/avail-go"
    ]

    import shutil
    for dir_path in sdk_dirs:
        try:
            if os.path.exists(dir_path):
                print(f"Removing directory: {dir_path}")
                shutil.rmtree(dir_path)
                print(f"Successfully removed {dir_path}")
            else:
                print(f"Directory {dir_path} does not exist, skipping")
        except Exception as e:
            print(f"Error removing directory {dir_path}: {e}")

    print("\n=== Cleanup completed ===")


    print("\n=== Script execution completed ===")

finally:
    # Restore stdout
    sys.stdout = output_capturer.terminal
    
    # Write all captured output to the log file
    try:
        with open(LOG_FILE, 'w') as f:
            f.write(output_capturer.get_content())
        print(f"Saved complete log to {LOG_FILE}")
        
        # Push the results and logs to GitHub
        push_success = push_to_github()
        if push_success:
            print("\n=== Git operations completed successfully ===")
        else:
            print("\n=== Git operations failed ===")
            
    except Exception as e:
        print(f"Error saving log file: {e}")