from pathlib import Path

TESTS_DIR = Path(__file__).parent
INPUT_FILES_DIR = TESTS_DIR / "input_files"
JSON_RESPONSES_DIR = INPUT_FILES_DIR / "json_responses"
PROJECT_DIR = TESTS_DIR.parent

GOOGLE_LOGIN_RESPONSE_PATH = JSON_RESPONSES_DIR / "google_login_response.json"
GOOGLE_TOKEN_RESPONSE_PATH = JSON_RESPONSES_DIR / "google_token_response.json"
OKTA_LOGIN_RESPONSE_PATH = JSON_RESPONSES_DIR / "okta_login_response.json"
