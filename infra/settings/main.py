from pydantic import BaseSettings
from settings.app import APP_SETTINGS, AppSettings
from settings.aws import AWS_SETTINGS, AWSSettings
from settings.network import NETWORK_SETTINGS, NetworkSettings
from settings.sentry import SENTRY_SETTINGS, SentrySettings
from settings.slack import SLACK_SETTINGS, SlackSettings
from settings.vercel import VERCEL_SETTINGS, VercelSettings


class Settings(BaseSettings):
    aws: AWSSettings = AWS_SETTINGS
    app: AppSettings = APP_SETTINGS
    network: NetworkSettings = NETWORK_SETTINGS
    sentry: SentrySettings = SENTRY_SETTINGS
    slack: SlackSettings = SLACK_SETTINGS
    vercel: VercelSettings = VERCEL_SETTINGS


SETTINGS = Settings()

if __name__ == "__main__":
    print(SETTINGS)
