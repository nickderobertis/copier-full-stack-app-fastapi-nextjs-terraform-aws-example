from settings import SETTINGS, Settings


def fe(path: str | None = None, settings: Settings = SETTINGS) -> str:
    use_path = path or ""
    return f"{settings.url}/{use_path}"


def monitoring(path: str | None = None, settings: Settings = SETTINGS) -> str:
    use_path = path or ""
    return f"{settings.grafana_url}/{use_path}"
