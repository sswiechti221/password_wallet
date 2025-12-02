from dataclasses import dataclass

@dataclass
class Config:
    DEBUG: bool
    DEBUG_DB: bool
    
    DATABASE_FILE: str
    SECRET_KEY: str
    
DebugConfig: Config = Config(
    DEBUG=True,
    DEBUG_DB=True,
    DATABASE_FILE="sqlite:///password_wallet_dev.db",
    SECRET_KEY="dev",
)

ProdConfig: Config = Config(
    DEBUG=False,
    DEBUG_DB=False,
    DATABASE_FILE="sqlite:///password_wallet.db",
    SECRET_KEY="SUPER_SECRET_KEY_CHANGE_ME",
)

# Url
DEFAULT_REDIRECT_URL = "/"

# Paga - File name
HOME_PAGE = "home.html"
AUTH_MAIN_PAGE = "credentials.html"
