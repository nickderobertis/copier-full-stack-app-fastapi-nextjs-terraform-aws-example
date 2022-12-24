from settings.db import DB_SETTINGS, DBSettings


def db_uri(settings: DBSettings = DB_SETTINGS):
    return settings.uri
