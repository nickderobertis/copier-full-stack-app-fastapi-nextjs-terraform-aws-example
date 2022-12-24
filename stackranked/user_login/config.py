from pathlib import Path

ANALYSIS_DIR = Path(__file__).parent.parent / "Analysis"
GOOGLE_ANALYSIS_DIR = ANALYSIS_DIR / "Google"

ANALYSIS_DIR.mkdir(exist_ok=True, parents=True)
GOOGLE_ANALYSIS_DIR.mkdir(exist_ok=True, parents=True)
