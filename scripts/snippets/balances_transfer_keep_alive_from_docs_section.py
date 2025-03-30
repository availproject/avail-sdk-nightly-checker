import requests, os, re, subprocess, sys, json
from pathlib import Path
from datetime import datetime
import sys

# ADDED: Compute the directory where this script is located
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

# Import helper functions
from helper_functions import (
    process_sdk,
    print_results_summary
)
print("Script directory:", script_dir)


# Define the snippet name, success string, and URL
SNIPPET_NAME = "Balances Transfer Keep Alive from Docs Section"
SUCCESS_STRING = "Transfer completed successfully"
url = "https://raw.githubusercontent.com/availproject/docs/refs/heads/main/app/docs/build-with-avail/interact-with-avail-da/transfer-balances/page.mdx"

# Target directories for our environments
TS_TARGET_DIR = "/root/desktop/avail-js"
RUST_TARGET_DIR = "/root/desktop/avail-rust"
GO_TARGET_DIR = "/root/desktop/avail-go"

TS_TARGET_FILE = os.path.join(TS_TARGET_DIR, "your-file-name.ts")
RUST_TARGET_FILE = os.path.join(RUST_TARGET_DIR, "src", "main.rs")
GO_TARGET_FILE = os.path.join(GO_TARGET_DIR, "main.go")

# Process JavaScript SDK
def process_javascript():
    return process_sdk(
        sdk_type="js",
        snippet_name=SNIPPET_NAME,
        content_cmd="cmd1",
        run_cmd_id="cmd2",
        success_string=SUCCESS_STRING,
        target_file=TS_TARGET_FILE,
        target_dir=TS_TARGET_DIR,
        calling_script=__file__,
        url=url
    )

# Process Rust SDK
def process_rust():
    return process_sdk(
        sdk_type="rust",
        snippet_name=SNIPPET_NAME,
        content_cmd="cmd3",
        run_cmd_id="cmd4",
        success_string=SUCCESS_STRING,
        target_file=RUST_TARGET_FILE,
        target_dir=RUST_TARGET_DIR,
        calling_script=__file__,
        url=url
    )

# Process Go SDK
def process_go():
    return process_sdk(
        sdk_type="go",
        snippet_name=SNIPPET_NAME,
        content_cmd="cmd5",
        run_cmd_id="cmd6",
        success_string=SUCCESS_STRING,
        target_file=GO_TARGET_FILE,
        target_dir=GO_TARGET_DIR,
        calling_script=__file__,
        url=url
    )
def main():
    print(f"=== Running {SNIPPET_NAME} Test for All SDKs ===")
    
    # Process each SDK
    js_result = process_javascript()
    rust_result = process_rust()
    go_result = process_go()
    
    # Print results summary
    overall_result = print_results_summary(SNIPPET_NAME, js_result, rust_result, go_result)
    
    # Return exit code based on success (0) or failure (1)
    sys.exit(0 if overall_result else 1)

if __name__ == "__main__":
    main()