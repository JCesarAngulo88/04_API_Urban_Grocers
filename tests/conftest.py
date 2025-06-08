# tests/conftest.py

import pytest
import requests
import time
# No need for 'os' module here if you're directly importing URL_SERVICE
# from configuration.py

# Import the base service URL and potentially other paths from your configuration.py
# Make sure your project structure allows this import (e.g., configuration.py is in the project root)
from config import configuration # Adjust import if configuration.py is in a subfolder


import logging
import sys # Needed for StreamHandler

# --- Your existing fixtures (api_server_ready, test_name, etc.) would go here ---

# --- Logging Configuration ---
# Get the root logger
# --- Logging Configuration ---
# Get the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO) # <-- CHANGE THIS TO INFO or WARNING

# Check if handlers already exist to prevent adding them multiple times
if not logger.handlers:
    # Create a handler to send logs to the console (standard output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO) # <-- CHANGE THIS TO INFO or WARNING (match logger level)

    # Define the format of your log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

# --- End Logging Configuration ---


@pytest.fixture(scope="session")
def api_server_ready():
    max_retries = 15
    retry_delay_seconds = 5

    # Use the URL_SERVICE directly from your configuration.py
    base_url = configuration.URL_SERVICE + configuration.DOC_PATH

    # --- DETERMINE YOUR HEALTH CHECK ENDPOINT ---
    # This is the most crucial part now.
    # Option A: If there's a dedicated /health endpoint at the service root (most common for health checks)
    #health_endpoint = f"{base_url}/health"

    # Option B: If there is NO dedicated /health endpoint, use a known, simple GET endpoint that should always respond.
    # For example, if GET /api/v1/users/ always returns a 200 OK (even an empty list)
    # health_endpoint = f"{base_url}{CREATE_USER_PATH}"

    # Option C: Just check the base URL itself if it's meant to respond to a GET
    # health_endpoint = base_url

    # For now, let's stick with Option A (common /health endpoint).
    # If this still fails, we'll need to confirm what a 'ready' endpoint truly is for Urban Grocers.

    print(f"\n--- Checking API server readiness at: {base_url} ---")

    for attempt in range(1, max_retries + 1):
        try:
            # Set a reasonable timeout for the request itself
            response = requests.get(base_url, timeout=10)

            if response.status_code == 200:
                print(f"API server is ready! (Attempt {attempt}/{max_retries})")
                return # Server is ready, fixture passes
            else:
                print(f"API server returned status {response.status_code}. "
                      f"Retrying in {retry_delay_seconds}s (Attempt {attempt}/{max_retries})...")
                # Optional: print response text to debug non-200 status codes
                # print(f"Response text: {response.text[:200]}...") # Print first 200 chars

        except requests.exceptions.ConnectionError:
            print(f"Connection refused/error to API server (URL: {base_url}). "
                  f"Retrying in {retry_delay_seconds}s (Attempt {attempt}/{max_retries})...")
        except requests.exceptions.Timeout:
            print(f"Connection timed out to API server (URL: {base_url}). "
                  f"Retrying in {retry_delay_seconds}s (Attempt {attempt}/{max_retries})...")
        except Exception as e:
            print(f"An unexpected error occurred during health check: {e} (URL: {base_url}). "
                  f"Retrying in {retry_delay_seconds}s (Attempt {attempt}/{max_retries})...")

        time.sleep(retry_delay_seconds)

    pytest.fail(f"ERROR: API server did not become ready after {max_retries} attempts. Tests cannot proceed.")