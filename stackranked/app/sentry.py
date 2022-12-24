from logger import log
from settings.main import SETTINGS, Settings


def init_sentry(settings: Settings = SETTINGS) -> None:
    if not settings.sentry_dsn:
        log.warn("Sentry DSN not set, skipping Sentry initialization")

    import sentry_sdk

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.05,
    )
    log.info("Sentry initialized")
