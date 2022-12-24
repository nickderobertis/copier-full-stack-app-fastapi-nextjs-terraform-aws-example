import app.all_models  # noqa: F401
from app.auth.backend import auth_backend
from app.auth.db import User
from app.auth.delete_router import delete_me_router
from app.auth.oauth.google.client import GoogleOAuthConfig
from app.auth.oauth.google.client import (
    google_oauth_config as default_google_oauth_config,
)
from app.auth.oauth.google.connected_router import create_google_connected_router
from app.auth.router import current_active_user, fastapi_users
from app.auth.schemas import UserCreate, UserRead, UserUpdate
from app.sentry import init_sentry
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings.main import SETTINGS

init_sentry()


def create_app(
    google_oauth_config: GoogleOAuthConfig = default_google_oauth_config,
) -> FastAPI:
    app = FastAPI()

    # TODO: restrict CORS
    origins: list[str] = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
    )
    if google_oauth_config is not None:
        app.include_router(
            fastapi_users.get_oauth_router(
                google_oauth_config.client,
                auth_backend,
                google_oauth_config.jwt_secret,
                redirect_url=f"{SETTINGS.fe_url}/auth/google",
                associate_by_email=True,
            ),
            prefix="/auth/google",
            tags=["auth"],
        )
        app.include_router(
            fastapi_users.get_oauth_associate_router(
                google_oauth_config.client,
                UserRead,
                google_oauth_config.jwt_secret,
                redirect_url=f"{SETTINGS.fe_url}/auth/google",
            ),
            prefix="/auth/associate/google",
            tags=["auth"],
        )
        app.include_router(
            create_google_connected_router(),
            prefix="/auth/connected/google",
            tags=["auth"],
        )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )
    app.include_router(
        delete_me_router,
        prefix="/delete-me",
        tags=["delete", "me", "user"],
    )

    if SETTINGS.enable_dev_endpoints:
        from app.dev.routes import dev_router

        app.include_router(dev_router, prefix="/dev", tags=["dev"])

    @app.get("/health-check")
    async def health_check():
        return {"success": True}

    @app.get("/authenticated-route")
    async def authenticated_route(user: User = Depends(current_active_user)):
        return {"message": f"Hello {user.email}!!"}

    @app.on_event("startup")
    async def on_startup():
        pass

    return app
