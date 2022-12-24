from pathlib import Path

DATA_FOLDER = Path(__file__).parent.parent / "Data"
GOOGLE_DATA_FOLDER = DATA_FOLDER / "Google"

CONVERTED_FOLDER = DATA_FOLDER / "Converted"
GOOGLE_CONVERTED_FOLDER = CONVERTED_FOLDER / "Google"
OKTA_CONVERTED_FOLDER = CONVERTED_FOLDER / "Okta"

GOOGLE_DATA_FOLDER.mkdir(exist_ok=True, parents=True)
GOOGLE_CONVERTED_FOLDER.mkdir(exist_ok=True, parents=True)
OKTA_CONVERTED_FOLDER.mkdir(exist_ok=True, parents=True)
