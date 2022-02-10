from os import environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    API_ID = int(environ.get("API_ID"))
    API_HASH = str(environ.get("API_HASH"))
    SESSION_STRING = str(environ.get("SESSION_STRING"))
    CHANNEL_ID = int(environ.get("CHANNEL_ID"))
    RCLONE_PASS = str(environ.get("RCLONE_PASS"))
    chat_Id = int(environ.get("chat_Id"))
    SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))  # 1 minte
    PORT = int(environ.get("PORT", 8080))
    BOT_TOKEN = str(environ.get("BOT_TOKEN"))
    BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    HAS_SSL = environ.get("HAS_SSL", False)
    HAS_SSL = True if str(HAS_SSL).lower() == "true" else False
    NO_PORT = environ.get("NO_PORT", False)
    NO_PORT = True if str(NO_PORT).lower() == "true" else False
    if "DYNO" in environ:
        ON_HEROKU = True
        APP_NAME = str(environ.get("APP_NAME"))
    else:
        ON_HEROKU = False
    FQDN = (str(environ.get("FQDN", BIND_ADDRESS)) if not ON_HEROKU
            or environ.get("FQDN") else APP_NAME + ".herokuapp.com")
    if ON_HEROKU:
        URL = f"https://{FQDN}/"
    else:
        URL = "http{}://{}{}/".format("s" if HAS_SSL else "", FQDN,
                                      "" if NO_PORT else ":" + str(PORT))
