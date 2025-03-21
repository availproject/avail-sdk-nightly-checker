import requests, os, re, subprocess, sys, json
from pathlib import Path
from datetime import datetime
import sys

# Compute the directory where this script is located
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

# URL of the raw markdown file for da-create-application-key
url = "https://raw.githubusercontent.com/availproject/docs/refs/heads/main/app/api-reference/avail-node-api/da-create-application-key/page.mdx"

# Generate unique timestamp for application keys
today_date = datetime.now().strftime("%d-%m-%Y")
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def process_javascript():
    """Process JavaScript SDK application key creation"""
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
    
    # Modify the key to be unique with timestamp
    unique_key = f"avail-js-automated-run-check-{today_date}-{current_timestamp}"
    ts_code = re.sub(
        r'(const\s+key\s*=\s*")[^"]*(")',
        rf'\1{unique_key}\2',
        ts_code
    )
    print(f"Set unique application key: {unique_key}")
    
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
    
    # Check for success by examining output
    if cmd_result and cmd_result.returncode == 0:
        output_lines = cmd_result.stdout.strip().splitlines()
        if len(output_lines) > 2:
            # Check the third line
            try:
                third_line = output_lines[2].strip()
                print("Third line of output:", third_line)
                if "Application created successfully" in third_line:
                    result = True
                    print("JavaScript application key creation was successful!")
            except IndexError:
                print("Output format unexpected, couldn't find success message")
        else:
            print("Insufficient output from TypeScript execution")
    else:
        print("JavaScript application key creation failed or didn't complete successfully")
    
    update_result("avail_js", result, __file__)
    return result

def process_rust():
    """Process Rust SDK application key creation"""
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
    
    # Modify the key to be unique with timestamp
    unique_key = f"avail-rust-automated-run-check-{today_date}-{current_timestamp}"
    rust_code = re.sub(
        r'(let\s+key\s*=\s*")[^"]*(")',
        rf'\1{unique_key}\2',
        rust_code
    )
    print(f"Set unique application key: {unique_key}")
    
    # Write the Rust code to the file
    try:
        with open(RUST_TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(rust_code)
        print(f"Successfully wrote Rust code to {RUST_TARGET_FILE}")
    except Exception as e:
        print(f"Error writing to Rust file: {e}")
        update_result("avail_rust", result, __file__)
        return result
    
    # Extract the run command (cmd4)
    run_cmd = extract_command(markdown, "cmd4")
    if not run_cmd:
        print("Run command (cmd4) not found in markdown")
        update_result("avail_rust", result, __file__)
        return result
    
    # Run the command
    cmd_result = run_command(run_cmd, RUST_TARGET_DIR)
    
    # Check for success by examining output
    if cmd_result and cmd_result.returncode == 0:
        output_lines = cmd_result.stdout.strip().splitlines()
        if len(output_lines) > 1:
            try:
                # Try to check second last line
                second_last_line = output_lines[-2].strip()
                print("Second last line of output:", second_last_line)
                if "Application Key Created" in second_last_line:
                    result = True
                    print("Rust application key creation was successful!")
            except IndexError:
                print("Output format unexpected, couldn't find success message")
        else:
            print("Insufficient output from Rust execution")
    else:
        print("Rust application key creation failed or didn't complete successfully")
    
    update_result("avail_rust", result, __file__)
    return result

def process_go():
    """Process Go SDK application key creation"""
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
    
    # Modify the key to be unique with timestamp
    unique_key = f"avail-go-automated-run-check-{today_date}-{current_timestamp}"
    go_code = re.sub(
        r'(key\s*:=\s*")[^"]*(")',
        rf'\1{unique_key}\2',
        go_code
    )
    print(f"Set unique application key: {unique_key}")
    
    # Write the Go code to the file
    try:
        with open(GO_TARGET_FILE, "w", encoding="utf-8") as f:
            f.write(go_code)
        print(f"Successfully wrote Go code to {GO_TARGET_FILE}")
    except Exception as e:
        print(f"Error writing to Go file: {e}")
        update_result("avail_go", result, __file__)
        return result
    
    # Extract the run command (cmd6)
    run_cmd = extract_command(markdown, "cmd6")
    if not run_cmd:
        print("Run command (cmd6) not found in markdown")
        update_result("avail_go", result, __file__)
        return result
    
    # Run the go command
    cmd_result = run_command(run_cmd, GO_TARGET_DIR)
    
    # Check for success by examining output
    if cmd_result and cmd_result.returncode == 0:
        output_lines = cmd_result.stdout.strip().splitlines()
        if len(output_lines) > 0:
            last_line = output_lines[-1].strip()
            print("Last line of output:", last_line)
            if "Application Key Created" in last_line:
                result = True
                print("Go application key creation was successful!")
        else:
            print("No output from Go execution")
    else:
        print("Go application key creation failed or didn't complete successfully")
    
    update_result("avail_go", result, __file__)
    return result

def main():
    print("=== Running DA Create Application Key Test for All SDKs ===")
    
    # Process each SDK
    js_result = process_javascript()
    rust_result = process_rust()
    go_result = process_go()
    
    # Print summary of results
    print("\n=== Test Results Summary ===")
    print(f"JavaScript DA Create Application Key: {'✅ Success' if js_result else '❌ Failed'}")
    print(f"Rust DA Create Application Key: {'✅ Success' if rust_result else '❌ Failed'}")
    print(f"Go DA Create Application Key: {'✅ Success' if go_result else '❌ Failed'}")
    
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
