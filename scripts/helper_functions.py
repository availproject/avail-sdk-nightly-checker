import os
import re
import json
import requests
import subprocess
from datetime import datetime

# Path to the results JSON file
RESULTS_FILE = "/root/desktop/run-results.json"

def fetch_markdown(url):
    """Fetch the markdown content from the given URL"""
    print(f"Fetching markdown from {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching markdown: {response.status_code}")
        return None
    return response.text

def extract_content(markdown, content_name, language="typescript"):
    """Extract content from markdown by name for different languages"""
    patterns = {
        "typescript": f'```typescript showLineNumbers filename="avail-js" name="{content_name}"\\s+(.*?)\\s+```',
        "rust": f'```rust showLineNumbers filename="avail-rust" name="{content_name}"\\s+(.*?)\\s+```',
        "go": f'```go showLineNumbers filename="avail-go" name="{content_name}"\\s+(.*?)\\s+```'
    }
    
    pattern = patterns.get(language, patterns["typescript"])
    match = re.search(pattern, markdown, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_command(markdown, cmd_name):
    """Extract a specific terminal command from markdown by name"""
    pattern = f'```bash filename="terminal" name="{cmd_name}"\\s+(.*?)\\s+```'
    match = re.search(pattern, markdown, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def run_command(command, directory):
    """Run the command in the specified directory"""
    print(f"Running command in {directory}: {command}")
    
    try:
        result = subprocess.run(
            command.split(),
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=45  # wait up to 45 seconds
        )
        
        # Print command output
        print("Command output:")
        print(result.stdout)
        
        if result.stderr:
            print("Error output:")
            print(result.stderr)
        
        return result
    except subprocess.TimeoutExpired:
        print("Command execution timed out")
        return None
    except Exception as e:
        print(f"Error executing command: {e}")
        return None

def read_results(calling_script_path):
    """
    Read the current results from the JSON file.
    Ensures required keys exist without overwriting the file.
    """
    # Extract the script name without extension or path
    script_name = os.path.splitext(os.path.basename(calling_script_path))[0]
    
    # Only attempt to read if the file exists
    if os.path.exists(RESULTS_FILE):
        try:
            # Read the existing JSON file
            with open(RESULTS_FILE, 'r') as f:
                results_data = json.load(f)
            
            # Make sure 'results' key exists
            if 'results' not in results_data:
                results_data['results'] = {}
            
            # Ensure required keys exist for all SDKs based on script name
            sdk_keys = [
                f"avail_js_{script_name}",
                f"avail_rust_{script_name}",
                f"avail_go_{script_name}"
            ]
            
            # Add any missing keys with default false value
            for key in sdk_keys:
                if key not in results_data['results']:
                    print(f"Adding missing key: {key}")
                    results_data['results'][key] = False
            
            return results_data
            
        except Exception as e:
            print(f"Error reading results file: {e}")
            # Return None on error, so caller knows there was a problem
            return None
    else:
        print(f"Results file {RESULTS_FILE} does not exist")
        return None

def update_result(sdk_prefix, value, calling_script_path):
    """
    Update a specific result in the JSON file
    sdk_prefix should be 'avail_js', 'avail_rust', or 'avail_go'
    """
    # Extract the script name without extension or path
    script_name = os.path.splitext(os.path.basename(calling_script_path))[0]
    
    # Construct the full key
    key = f"{sdk_prefix}_{script_name}"
    
    # Get current results
    results_data = read_results(calling_script_path)
    
    # If results were read successfully
    if results_data:
        # Update the specific key
        results_data["results"][key] = value
        
        # Update timestamp
        results_data["last_run_timestamp"] = datetime.now().isoformat()
        
        try:
            # Write the updated results back to the file
            with open(RESULTS_FILE, 'w') as f:
                json.dump(results_data, f, indent=2)
            print(f"Updated {key} result to {value}")
            return True
        except Exception as e:
            print(f"Error updating results file: {e}")
    
    return False