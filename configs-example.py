import os

SQLITE_CONN_STR = os.environ.get("SQLITE_CONN_STR", ":memory:")

REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", 5))
WALLEX_AUTH_TOKEN = os.environ["WALLEX_AUTH_TOKEN"]

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
