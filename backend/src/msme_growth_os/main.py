from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from msme_growth_os.core.config import get_settings
from msme_growth_os.interfaces.api.v1.router import api_v1_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
