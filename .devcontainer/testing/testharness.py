import subprocess
import os, threading
from helpers import *

DT_API_TOKEN_TESTING = os.getenv("DT_API_TOKEN_TESTING","")

# Use the main token
# To create short lived tokens
# To run the test harness
# Use these short-lived tokens during the test harness.
DT_TENANT_APPS, DT_TENANT_LIVE = build_dt_urls(dt_env_id=DT_ENVIRONMENT_ID, dt_env_type=DT_ENVIRONMENT_TYPE)
DT_API_TOKEN_TO_USE = create_dt_api_token(token_name="[devrel e2e testing] DT_LOG_PROBLEM_DETECTION_E2E_TEST_TOKEN", scopes=["logs.ingest", "metrics.ingest", "openTelemetryTrace.ingest", "events.ingest"], dt_rw_api_token=DT_API_TOKEN_TESTING, dt_tenant_live=DT_TENANT_LIVE)
# store_env_var(key="DT_API_TOKEN", value=DT_API_TOKEN_TO_USE)

# The secret will already exist from environment_installer
# So delete it first then recreate it
run_command(["kubectl", "delete", "secret", "dynatrace-otelcol-dt-api-credentials"])
run_command(["kubectl", "create", "secret", "generic", "dynatrace-otelcol-dt-api-credentials", f"--from-literal=DT_ENDPOINT={DT_TENANT_LIVE}/api/v2/otlp", f"--from-literal=DT_API_TOKEN={DT_API_TOKEN_TO_USE}"])
# Now restart collector to pick up new secret
run_command(["kubectl", "scale", "deploy", "dynatrace-collector-opentelemetry-collector", "--replicas", "0"])
run_command(["kubectl", "scale", "deploy", "dynatrace-collector-opentelemetry-collector", "--replicas", "1"])

if DEV_MODE:
    steps = get_steps("steps.txt")
else:
    steps = get_steps(f"/workspaces/{REPOSITORY_NAME}/.devcontainer/testing/steps.txt")
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

    if step.startswith("//") or step.startswith("#"):
        print(f"[{step}] Ignore this step. It is commented out.")
        continue
    
    if "test_" in step:
        print(f"[{step}] This step is a Playwright test.")
        if DEV_MODE == "FALSE": # Standard mode. Run test headlessly
            output = subprocess.run(["pytest", "--capture=no", f"{TESTING_BASE_DIR}/{step}"], capture_output=True, text=True)
        else: # Interactive mode (when a maintainer is improving testing. Spin up the browser visually.
            output = subprocess.run(["pytest", "--capture=no", "--headed", f"{TESTING_BASE_DIR}/{step}"], capture_output=True, text=True)

        if output.returncode != 0 and DEV_MODE == "FALSE":
            logger.error(f"Must create an issue: {step} {output}")
            create_github_issue(output, step_name=step)
        else:
            print(output)
    else:
        output = subprocess.run(["runme", "run", step], capture_output=True, text=True)
        print(f"[{step}] | {output.returncode} | {output.stdout}")
        if output.returncode != 0 and DEV_MODE == "FALSE":
            logger.error(f"Must create an issue: {step} {output}")
            create_github_issue(output, step_name=step)
        else:
            print(output)