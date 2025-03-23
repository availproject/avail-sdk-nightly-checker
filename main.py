#!/usr/bin/env python
import subprocess
import re
import sys
import os
import json
from datetime import datetime

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

try:

    # Force scripts to flush output immediately
    env = os.environ.copy()
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

    # Executing the data submission script
    print("\n=== Running data submission script ===")

    da_submit_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts/snippets/da_submit_data.py")

    # Execute the script as a subprocess with real-time output streaming
    print("Data submission script output:")
    try:
        # Use a different approach to run the script to get real-time output
        process = subprocess.Popen(
            ["python", da_submit_script],
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
        print(f"\nData submission script completed with return code: {return_code}")
        
    except Exception as e:
        print(f"Error running data submission script: {e}")

    print("\n================================================")

    # Executing the create application key script
    print("\n=== Running create application key script ===")

    da_create_application_key_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts/snippets/da_create_application_key.py")
    
    # Execute the script as a subprocess with real-time output streaming
    print("Create application key script output:")
    try:
        # Use a different approach to run the script to get real-time output
        process = subprocess.Popen(
            ["python", da_create_application_key_script],
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
        print(f"\nCreate application key script completed with return code: {return_code}")
        
    except Exception as e:
        print(f"Error running create application key script: {e}")

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

    # # Push results to Git repository
    # print("\n=== Pushing results to Git repository ===")
    # try:
    #     # Get current timestamp for commit message
    #     current_time = datetime.now().isoformat()
        
    #     # Change to the desktop directory where the Git repository is initialized
    #     git_commands = [
    #         ["git", "add", "run-results.json", "last-run-log.txt"],
    #         ["git", "commit", "-m", f"Pushing log result of run at {current_time}"],
    #         ["git", "push", "origin", "main"]
    #     ]
        
    #     for cmd in git_commands:
    #         print(f"Running: {' '.join(cmd)}")
    #         result = subprocess.run(
    #             cmd,
    #             cwd="/root/desktop",
    #             capture_output=True,
    #             text=True
    #         )
            
    #         if result.returncode == 0:
    #             print(f"Command succeeded: {result.stdout.strip()}")
    #         else:
    #             print(f"Command failed with return code {result.returncode}")
    #             print(f"Error: {result.stderr.strip()}")
    #             print("Continuing with next steps...")
        
    #     # For push, we have options:
    #     # OPTION 1: Using environment variable for GitHub token (RECOMMENDED)
    #     # Set GITHUB_TOKEN environment variable before running the script
    #     github_token = os.environ.get("GITHUB_TOKEN")
    #     if github_token:
    #         print("Running: git push (with token from environment)")
    #         # Construct the URL with the token
    #         repo_url = f"https://{github_token}@github.com/availproject/avail-sdk-nightly-checker.git"
    #         result = subprocess.run(
    #             ["git", "push", repo_url, "main"],
    #             cwd="/root/desktop",
    #             capture_output=True,
    #             text=True
    #         )
    #     else:
    #         # OPTION 2: Fall back to regular push (requires pre-configured credentials)
    #         print("Running: git push origin main (requires pre-configured credentials)")
    #         print(For cron jobs, this may fail unless credentials are properly configured")
    #         result = subprocess.run(
    #             ["git", "push", "origin", "main"],
    #             cwd="/root/desktop",
    #             capture_output=True,
    #             text=True
    #         )
        
    #     if result.returncode == 0:
    #         print(f"Push succeeded: {result.stdout.strip()}")
    #     else:
    #         print(f"Push failed with return code {result.returncode}")
    #         print(f"Error: {result.stderr.strip()}")
        
    #     print("Git push completed")
    # except Exception as e:
    #     print(f"Error during Git operations: {e}")
    #     print("Continuing with next steps...")
    
    print("\n=== Script execution completed ===")

finally:
    # Restore stdout
    sys.stdout = output_capturer.terminal
    
    # Write all captured output to the log file
    try:
        with open(LOG_FILE, 'w') as f:
            f.write(output_capturer.get_content())
        print(f"Saved complete log to {LOG_FILE}")
    except Exception as e:
        print(f"Error saving log file: {e}")