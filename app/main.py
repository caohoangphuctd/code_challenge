from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.__version__ import __version__
from app.apis import configure_routes
from app.config import config
from app.configure_logging import configure_logging
from app.exceptions.handle_exceptions import configure_exceptions_handlers

# Create instance of application
app = FastAPI(
    title=config.APPLICATION_NAME,
    description=config.DESCRIPTION,
    version=__version__,
    debug=config.DEBUG,
    docs_url=config.OPENAPI_PREFIX,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update and set up configs
configure_logging(log_level=config.LOG_LEVEL)
configure_exceptions_handlers(app)

# Configure routes and add dependencies
configure_routes(app)
