import os
from dotenv import dotenv_values, find_dotenv

# Load .env
env_file = find_dotenv(".env")
config_env = dotenv_values(env_file)

# Base paths
# Use absolute path to ensure the right folder path
BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
# write uploads outside the root folder for safety
UPLOAD_FOLDER = os.path.join(BASE_FOLDER, "..", "uploads")


class Config:
    # Flask
    SECRET_KEY = config_env["FLASK_BIBLIOTEKA_DOMOWA_SECRET_KEY"]

    # Uploads
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    CHUNK_SIZE_BYTES = 1 * 1024  # 1 KB

    # Database
    db_rel_path = str(config_env["FLASK_BIBLIOTEKA_DOMOWA_DB"])
    db_path = os.path.join(BASE_FOLDER, db_rel_path)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API access
    ADMIN_SECRET_KEY = config_env[
        "FLASK_BIBLIOTEKA_DOMOWA_API_ADMIN_SECRET_KEY"
    ]

    # Allowed picture attributes
    ALLOWED_EXT = {
        "png": {"soi": b"\x89PNG\r\n\x1a\n", "eoi": b""},
        "jpg": {"soi": b"\xff\xd8", "eoi": b"\xff\xd9"},
        "gif": {"soi87a": b"GIF87a", "soi89a": b"GIF89a", "eoi": b""},
    }

    EXT_ALIASES = {
        "jpeg": "jpg",
        "tif": "tiff",
    }

    print("ENV FILE:", env_file)
    print("CONFIG ENV:", config_env)