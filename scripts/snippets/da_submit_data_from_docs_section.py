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
    update_result,
    process_sdk
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

# URL of the raw markdown file for da-submit-data
url = "https://raw.githubusercontent.com/availproject/docs/refs/heads/main/app/docs/build-with-avail/interact-with-avail-da/read-write-on-avail/page.mdx"

# Process JavaScript SDK
def process_javascript():
    return process_sdk(
        sdk_type="js",
        snippet_name="Data Submission from Docs Section",
        content_cmd="cmd1",
        run_cmd_id="cmd2",
        success_string="Data submission completed successfully",
        target_file=TS_TARGET_FILE,
        target_dir=TS_TARGET_DIR,
        calling_script=__file__,
        url=url
    )

# Process Rust SDK
def process_rust():
    return process_sdk(
        sdk_type="rust",
        snippet_name="Data Submission from Docs Section",
        content_cmd="cmd3",
        run_cmd_id="cmd4",
        success_string="Data Submission finished correctly",
        target_file=RUST_TARGET_FILE,
        target_dir=RUST_TARGET_DIR,
        calling_script=__file__,
        url=url
    )

# Process Go SDK
def process_go():
    return process_sdk(
        sdk_type="go",
        snippet_name="Data Submission from Docs Section",
        content_cmd="cmd5",
        run_cmd_id="cmd6",
        success_string="Data submission completed successfully",
        target_file=GO_TARGET_FILE,
        target_dir=GO_TARGET_DIR,
        calling_script=__file__,
        url=url
    )

def main():
    print("=== Running DA Submit Data Test for All SDKs ===")
    
    # Process each SDK
    js_result = process_javascript()
    rust_result = process_rust()
    go_result = process_go()
    
    # Print summary of results
    print("\n=== Test Results Summary ===")
    print(f"JavaScript DA Submit Data: {'✅ Success' if js_result else '❌ Failed'}")
    print(f"Rust DA Submit Data: {'✅ Success' if rust_result else '❌ Failed'}")
    print(f"Go DA Submit Data: {'✅ Success' if go_result else '❌ Failed'}")
    
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