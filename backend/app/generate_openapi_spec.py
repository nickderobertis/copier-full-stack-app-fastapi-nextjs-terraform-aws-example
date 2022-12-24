import json
from pathlib import Path

from app.main import app
from fastapi import FastAPI
from logger import log

OPENAPI_SPEC_PATH = Path(__file__).parent / "openapi.json"


def generate_openapi_spec(fastapi: FastAPI = app, path: Path = OPENAPI_SPEC_PATH):
    path.write_text(json.dumps(fastapi.openapi()))


if __name__ == "__main__":
    log.info("Generating OpenAPI spec")
    generate_openapi_spec()
