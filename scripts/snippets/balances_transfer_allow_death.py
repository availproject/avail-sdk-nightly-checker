import requests, os, re, subprocess, sys, json
from pathlib import Path
from datetime import datetime
import sys

# ADDED: Compute the directory where this script is located
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

# Import helper functions
from helper_functions import (
    fetch_markdown, 
    extract_content, 
    extract_command,
    run_command,
    update_result
)
print("Script directory:", script_dir)

# Target directories for our environments
TS_TARGET_DIR = "/root/desktop/avail-js"
RUST_TARGET_DIR = "/root/desktop/avail-rust"
GO_TARGET_DIR = "/root/desktop/avail-go"

TS_TARGET_FILE = os.path.join(TS_TARGET_DIR, "your-file-name.ts")
RUST_TARGET_FILE = os.path.join(RUST_TARGET_DIR, "src", "main.rs")
GO_TARGET_FILE = os.path.join(GO_TARGET_DIR, "main.go")

# Path to the results JSON file
RESULTS_FILE = "/root/desktop/run-results.json"

# URL of the raw markdown file for balances-transfer-allow-death
url = "https://raw.githubusercontent.com/availproject/docs/refs/heads/main/app/api-reference/avail-node-api/balances-transfer-allow-death/page.mdx"


def process_javascript():
    """Process JavaScript SDK balances transfer allow death"""
    print("\n===== Processing JavaScript SDK =====")
    result = False
    
    markdown = fetch_markdown(url)
    if not markdown:
        update_result("avail_js", result, __file__)
        return result
    
    # Check if the TypeScript file exists
    if not os.path.exists(TS_TARGET_FILE):
        print(f"Error: Target TypeScript file {TS_TARGET_FILE} does not exist")
        update_result("avail_js", result, __file__)
        return result
    
    # Wipe the contents of the TypeScript file
    try:
        with open(TS_TARGET_FILE, "w", encoding="utf-8") as f:
            f.write("")  # Write empty string to clear the file
        print(f"Successfully wiped contents of {TS_TARGET_FILE}")
    except Exception as e:
        print(f"Error wiping contents of TypeScript file: {e}")
        update_result("avail_js", result, __file__)
        return result
    
    # Extract TypeScript code (cmd1)
    ts_code = extract_content(markdown, "cmd1", "typescript")
    if not ts_code:
        print("TypeScript code (cmd1) not found in markdown")
        update_result("avail_js", result, __file__)
        return result
    
    # Write the TypeScript code to the file
    try:
        with open(TS_TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(ts_code)
        print(f"Successfully wrote TypeScript code to {TS_TARGET_FILE}")
    except Exception as e:
        print(f"Error writing to TypeScript file: {e}")
        update_result("avail_js", result, __file__)
        return result
    
    # Extract the run command (cmd2)
    run_cmd = extract_command(markdown, "cmd2")
    if not run_cmd:
        print("Run command (cmd2) not found in markdown")
        update_result("avail_js", result, __file__)
        return result
    
    # Run the command
    cmd_result = run_command(run_cmd, TS_TARGET_DIR)
    
    if cmd_result and cmd_result.returncode == 0 and "Transfer completed successfully" in cmd_result.stdout:
        result = True
        print("JavaScript transfer allow death was successful!")
    else:
        print("JavaScript transfer allow death failed or didn't complete successfully")
    
    update_result("avail_js", result, __file__)
    return result

def process_rust():
    """Process Rust SDK balances transfer allow death"""
    print("\n===== Processing Rust SDK =====")
    result = False
    
    markdown = fetch_markdown(url)
    if not markdown:
        update_result("avail_rust", result, __file__)
        return result
    
    # Check if the Rust file exists
    if not os.path.exists(RUST_TARGET_FILE):
        print(f"Error: Target Rust file {RUST_TARGET_FILE} does not exist")
        update_result("avail_rust", result, __file__)
        return result
    
    # Wipe the contents of the Rust file
    try:
        with open(RUST_TARGET_FILE, "w", encoding="utf-8") as f:
            f.write("")  # Write empty string to clear the file
        print(f"Successfully wiped contents of {RUST_TARGET_FILE}")
    except Exception as e:
        print(f"Error wiping contents of Rust file: {e}")
        update_result("avail_rust", result, __file__)
        return result
    
    # Extract Rust code (cmd3)
    rust_code = extract_content(markdown, "cmd3", "rust")
    if not rust_code:
        print("Rust code (cmd3) not found in markdown")
        update_result("avail_rust", result, __file__)
        return result
    
    # Write the Rust code to the file
    try:
        with open(RUST_TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(rust_code)
        print(f"Successfully wrote Rust code to {RUST_TARGET_FILE}")
    except Exception as e:
        print(f"Error writing to Rust file: {e}")
        update_result("avail_rust", result, __file__)
        return result
    
    # Extract the run command (cmd4) for Rust
    rust_run_cmd = extract_command(markdown, "cmd4")
    if not rust_run_cmd:
        print("Run command (cmd4) not found in markdown for Rust")
        update_result("avail_rust", result, __file__)
        return result
    
    # Run the extracted command
    cmd_result = run_command(rust_run_cmd, RUST_TARGET_DIR)
    
    if cmd_result and cmd_result.returncode == 0 and "transfer completed successfully" in cmd_result.stdout:
        result = True
        print("Rust transfer allow death was successful!")
    else:
        print("Rust transfer allow death failed or didn't complete successfully")
    
    update_result("avail_rust", result, __file__)
    return result

def process_go():
    """Process Go SDK balances transfer allow death"""
    print("\n===== Processing Go SDK =====")
    result = False
    
    markdown = fetch_markdown(url)
    if not markdown:
        update_result("avail_go", result, __file__)
        return result
    
    # Check if the Go file exists
    if not os.path.exists(GO_TARGET_FILE):
        print(f"Error: Target Go file {GO_TARGET_FILE} does not exist")
        update_result("avail_go", result, __file__)
        return result
    
    # Wipe the contents of the Go file
    try:
        with open(GO_TARGET_FILE, "w", encoding="utf-8") as f:
            f.write("")  # Write empty string to clear the file
        print(f"Successfully wiped contents of {GO_TARGET_FILE}")
    except Exception as e:
        print(f"Error wiping contents of Go file: {e}")
        update_result("avail_go", result, __file__)
        return result
    
    # Extract Go code (cmd5)
    go_code = extract_content(markdown, "cmd5", "go")
    if not go_code:
        print("Go code (cmd5) not found in markdown")
        update_result("avail_go", result, __file__)
        return result
    
    # Write the Go code to the file
    try:
        with open(GO_TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(go_code)
        print(f"Successfully wrote Go code to {GO_TARGET_FILE}")
    except Exception as e:
        print(f"Error writing to Go file: {e}")
        update_result("avail_go", result, __file__)
        return result
    
    # Extract the run command (cmd6) for Go
    go_run_cmd = extract_command(markdown, "cmd6")
    if not go_run_cmd:
        print("Run command (cmd6) not found in markdown for Go")
        update_result("avail_go", result, __file__)
        return result
    
    # Run the extracted command
    cmd_result = run_command(go_run_cmd, GO_TARGET_DIR)
    
    if cmd_result and cmd_result.returncode == 0 and "Transfer completed successfully" in cmd_result.stdout:
        result = True
        print("Go transfer allow death was successful!")
    else:
        print("Go transfer allow death failed or didn't complete successfully")
    
    update_result("avail_go", result, __file__)
    return result

def main():
    print("=== Running Balances Transfer Allow Death Test for All SDKs ===")
    
    # Process each SDK
    js_result = process_javascript()
    rust_result = process_rust()
    go_result = process_go()
    
    # Print summary of results
    print("\n=== Test Results Summary ===")
    print(f"JavaScript Balances Transfer Allow Death: {'✅ Success' if js_result else '❌ Failed'}")
    print(f"Rust Balances Transfer Allow Death: {'✅ Success' if rust_result else '❌ Failed'}")
    print(f"Go Balances Transfer Allow Death: {'✅ Success' if go_result else '❌ Failed'}")
    
    # Print machine-readable results for potential parsing by other scripts
    print("\nMachine-readable results:")
    print("js_snippetrunresult =", js_result)
    print("rust_snippetrunresult =", rust_result)
    print("go_snippetrunresult =", go_result)

    # Determine overall success/failure
    overall_result = js_result and rust_result and go_result
    print("\nOverall test result:", "✅ Success" if overall_result else "❌ Failed")
    
    # Return exit code based on success (0) or failure (1)
    sys.exit(0 if overall_result else 1)

if __name__ == "__main__":
    main()