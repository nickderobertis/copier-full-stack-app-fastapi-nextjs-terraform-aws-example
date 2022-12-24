from pathlib import Path

from datamodel_code_generator import InputFileType, generate

RESOURCES_PATH = Path(__file__).parent / "resources"
SENTRY_LIST_EVENT_SCHEMA = RESOURCES_PATH / "sentry-list-event-schema.json"

CODEGEN_OUT_PATH = Path(__file__).parent / "generated" / "models"
SENTRY_LIST_EVENT_MODELS_PATH = CODEGEN_OUT_PATH / "list_event.py"


def generate_sentry_event_models():
    generate(
        SENTRY_LIST_EVENT_SCHEMA,
        input_file_type=InputFileType.JsonSchema,
        output=SENTRY_LIST_EVENT_MODELS_PATH,
        class_name="SentryListEventResponse",
        force_optional_for_required_fields=True,
    )


if __name__ == "__main__":
    generate_sentry_event_models()
