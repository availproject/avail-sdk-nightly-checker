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

def read_results(calling_script_path, sdk_prefix=None):
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

            # If sdk_prefix is provided, only ensure that specific key exists
            if sdk_prefix:
                key = f"{sdk_prefix}_{script_name}"
                if key not in results_data['results']:
                    print(f"Adding missing key: {key}")
                    results_data['results'][key] = False
            else:
                # Original behavior for backward compatibility
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
    results_data = read_results(calling_script_path, sdk_prefix)
    
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

def process_sdk(
    sdk_type,          # "js", "rust", or "go"
    snippet_name,      # Name of the snippet (e.g., "System Account")
    content_cmd,       # Command id for code content (e.g., "cmd1")
    run_cmd_id,        # Command id for run command (e.g., "cmd2")
    success_string,    # String to check for success
    target_file,       # File to write code to
    target_dir, 
    calling_script,       # Directory for running commands
    url,                              # URL for markdown
):
    """Process SDK snippet execution and update results"""
    print(f"\n===== Processing {sdk_type.upper()} SDK {snippet_name} =====")
    result = False
    
    # Map SDK type to language for content extraction
    language_map = {"js": "typescript", "rust": "rust", "go": "go"}
    language = language_map.get(sdk_type.lower(), "typescript")
    
    # Determine result key
    result_key = f"avail_{sdk_type.lower()}"
    
    markdown = fetch_markdown(url)
    if not markdown:
        update_result(result_key, result, calling_script)
        return result
    
    # Check if target file exists
    if not os.path.exists(target_file):
        print(f"Error: Target file {target_file} does not exist")
        update_result(result_key, result, calling_script)
        return result
    
    # Wipe the contents of the file
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("")
        print(f"Successfully wiped contents of {target_file}")
    except Exception as e:
        print(f"Error wiping contents of file: {e}")
        update_result(result_key, result, calling_script)
        return result
    
    # Extract code content
    content = extract_content(markdown, content_cmd, language)
    if not content:
        print(f"Code content ({content_cmd}) not found in markdown")
        update_result(result_key, result, calling_script)
        return result
    
    # Write the code to the file
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully wrote code to {target_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        update_result(result_key, result, calling_script)
        return result
    
    # Extract the run command
    run_cmd = extract_command(markdown, run_cmd_id)
    if not run_cmd:
        print(f"Run command ({run_cmd_id}) not found in markdown")
        update_result(result_key, result, calling_script)
        return result
    
    # Run the command
    cmd_result = run_command(run_cmd, target_dir)
    
    if cmd_result and cmd_result.returncode == 0 and success_string in cmd_result.stdout:
        result = True
        print(f"{sdk_type.upper()} {snippet_name} was successful!")
    else:
        print(f"{sdk_type.upper()} {snippet_name} failed or didn't complete successfully")
    
    update_result(result_key, result, calling_script)
    return result

def print_results_summary(snippet_name, js_result, rust_result, go_result):
    """Print a standardized summary of test results for all SDKs."""
    print(f"\n=== Test Results Summary ===")
    print(f"JavaScript {snippet_name}: {'✅ Success' if js_result else '❌ Failed'}")
    print(f"Rust {snippet_name}: {'✅ Success' if rust_result else '❌ Failed'}")
    print(f"Go {snippet_name}: {'✅ Success' if go_result else '❌ Failed'}")
    
    # Print machine-readable results
    print("\nMachine-readable results:")
    print("js_snippetrunresult =", js_result)
    print("rust_snippetrunresult =", rust_result)
    print("go_snippetrunresult =", go_result)
    
    # Determine overall success/failure
    overall_result = js_result and rust_result and go_result
    print("\nOverall test result:", "✅ Success" if overall_result else "❌ Failed")
    
    return overall_result  # Return so the caller can use sys.exit()