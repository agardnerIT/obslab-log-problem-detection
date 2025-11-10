import subprocess
import os, threading
from helpers import *

DT_API_TOKEN_TESTING = os.getenv("DT_API_TOKEN_TESTING","")

# If testing token is not present
# Test harness cannot proceed, immediately exit
if DT_API_TOKEN_TESTING == "":
    logger.error("DT_API_TOKEN_TESTING is missing. Please define and re-execute the test harness.")
    exit(1)

# Use the main token
# To create short lived tokens
# To run the test harness
# Use these short-lived tokens during the test harness.
DT_TENANT_APPS, DT_TENANT_LIVE = build_dt_urls(dt_env_id=DT_ENVIRONMENT_ID, dt_env_type=DT_ENVIRONMENT_TYPE)
DT_API_TOKEN_TO_USE = create_dt_api_token(token_name="[devrel e2e testing] DT_SYSLOG_E2E_TEST_TOKEN", scopes=["logs.ingest"], dt_rw_api_token=DT_API_TOKEN_TESTING, dt_tenant_live=DT_TENANT_LIVE)
store_env_var(key="DT_API_TOKEN", value=DT_API_TOKEN_TO_USE)

steps = get_steps(f"{TESTING_BASE_DIR}/steps.txt")
INSTALL_PLAYWRIGHT_BROWSERS = False

def run_command_in_background(step):
    command = ["runme", "run", step]
    with open("nohup.out", "w") as f:
        subprocess.Popen(["nohup"] + command, stdout=f, stderr=f)

# Installing Browsers for Playwright is a time consuming task
# So only install if we need to
# That means if running in non-dev mode (dev mode assumes the person already has everything installed)
# AND the steps file actually contains a playwright test (no point otherwise!)
if DEV_MODE == "FALSE":
    for step in steps:
        if "test_" in step:
            INSTALL_PLAYWRIGHT_BROWSERS = True

if INSTALL_PLAYWRIGHT_BROWSERS:
    subprocess.run(["playwright", "install", "chromium-headless-shell", "--only-shell", "--with-deps"])

for step in steps:
    step = step.strip()
    logger.info(f"Running {step}")

    if step.startswith("//") or step.startswith("#"):
        logger.info(f"[{step}] Ignore this step. It is commented out.")
        continue
    
    if "test_" in step:
        logger.info(f"[{step}] This step is a Playwright test.")
        if DEV_MODE == "FALSE": # Standard mode. Run test headlessly
            output = subprocess.run(["pytest", "--capture=no", f"{TESTING_BASE_DIR}/{step}"], capture_output=True, text=True)
        else: # Interactive mode (when a maintainer is improving testing. Spin up the browser visually.
            output = subprocess.run(["pytest", "--capture=no", "--headed", f"{TESTING_BASE_DIR}/{step}"], capture_output=True, text=True)

        if output.returncode != 0 and DEV_MODE == "FALSE":
            send_business_event(output)
        else:
            logger.info(output)
    else:
        command = ["runme", "run", step]

        # If task should be run in background
        # TODO: This is tech debt
        # and should be refactored when
        # runme beta run supports backgrounding
        if "[background]" in step:
            # Run the command in the background and capture the output
            # Create a thread to run the command
            thread = threading.Thread(target=run_command_in_background, args=(step,))
            thread.start()
        else:
            print(f"Running: {command}")
            output = subprocess.run(command, capture_output=True, text=True)
            logger.info(output)
            if output.returncode != 0 and DEV_MODE == "FALSE":
                send_business_event(output)
            else:
                logger.info(output)
