import uuid
from typing import Optional, Type, TypeAlias, Union

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, InvalidPasswordException, UUIDIDMixin
from fastapi_users import exceptions as fapi_users_exceptions
from fastapi_users import models
from logger import log
from settings.main import SETTINGS

from .. import email
from .db import User, get_user_db
from .oauth.google.client import GoogleOAuthConfig, get_google_oauth_config
from .schemas import UserCreate

SECRET = "SECRET"

UserManager: TypeAlias = BaseUserManager[User, uuid.UUID]


def create_user_manager_class(
    google_oauth_config: GoogleOAuthConfig,
) -> Type[UserManager]:
    class _UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
        reset_password_token_secret = SECRET
        verification_token_secret = SECRET

        async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User],
        ) -> None:
            if len(password) < 8:
                raise InvalidPasswordException(
                    reason="Password should be at least 8 characters"
                )
            if user.email in password:
                raise InvalidPasswordException(
                    reason="Password should not contain e-mail"
                )

        async def on_after_register(
            self, user: User, request: Optional[Request] = None
        ):
            log.info(f"User {user.id} has registered.")

        async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
        ):
            reset_url = f"{SETTINGS.fe_url}/reset-password?token=" + token
            log.info(
                f"User {user.id} has forgot their password. Reset url: {reset_url}"
            )
            message = f"Please reset your password. Here is the link: <a href='{reset_url}'>{reset_url}</a>"
            # TODO: send email in background task
            await email.send_single(user.email, "Reset Password", message)

        async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
        ):
            log.info(
                f"Verification requested for user {user.id}. Verification token: {token}"
            )

        async def on_before_delete(
            self, user: models.UP, request: Optional[Request] = None
        ) -> None:
            log.info(f"User {user.id} is about to be deleted.")

        async def oauth_callback(
            self: "BaseUserManager[models.UOAP, models.ID]",
            oauth_name: str,
            access_token: str,
            account_id: str,
            account_email: str,
            expires_at: Optional[int] = None,
            refresh_token: Optional[str] = None,
            request: Optional[Request] = None,
            *,
            associate_by_email: bool = False,
        ) -> models.UOAP:
            """
            Handle the callback after a successful OAuth authentication.

            If the user already exists with this OAuth account, the token is updated.

            If a user with the same e-mail already exists and `associate_by_email` is True,
            the OAuth account is associated to this user.
            Otherwise, the `UserNotExists` exception is raised.

            If the user does not exist, it is created and the on_after_register handler
            is triggered.

            Note that this is a copy of the original method from fastapi-users, but
            it also extracts the user's name to be stored in the database.

            :param oauth_name: Name of the OAuth client.
            :param access_token: Valid access token for the service provider.
            :param account_id: models.ID of the user on the service provider.
            :param account_email: E-mail of the user on the service provider.
            :param expires_at: Optional timestamp at which the access token expires.
            :param refresh_token: Optional refresh token to get a
            fresh access token from the service provider.
            :param request: Optional FastAPI request that
            triggered the operation, defaults to None
            :param associate_by_email: If True, any existing user with the same
            e-mail address will be associated to this user. Defaults to False.
            :return: A user.
            """
            oauth_account_dict = {
                "oauth_name": oauth_name,
                "access_token": access_token,
                "account_id": account_id,
                "account_email": account_email,
                "expires_at": expires_at,
                "refresh_token": refresh_token,
            }

            try:
                user = await self.get_by_oauth_account(oauth_name, account_id)
            except fapi_users_exceptions.UserNotExists:
                try:
                    # Associate account
                    user = await self.get_by_email(account_email)
                    if not associate_by_email:
                        raise fapi_users_exceptions.UserAlreadyExists()
                    user = await self.user_db.add_oauth_account(
                        user, oauth_account_dict
                    )
                except fapi_users_exceptions.UserNotExists:
                    # Create account
                    user_details = await google_oauth_config.client.get_user_info(
                        access_token
                    )
                    password = self.password_helper.generate()
                    user_dict = {
                        "email": account_email,
                        "hashed_password": self.password_helper.hash(password),
                        "name": user_details.names[0].displayName,
                        "has_real_password": False,
                    }
                    user = await self.user_db.create(user_dict)
                    user = await self.user_db.add_oauth_account(
                        user, oauth_account_dict
                    )
                    await self.on_after_register(user, request)
            else:
                # Update oauth
                for existing_oauth_account in user.oauth_accounts:
                    if (
                        existing_oauth_account.account_id == account_id
                        and existing_oauth_account.oauth_name == oauth_name
                    ):
                        user = await self.user_db.update_oauth_account(
                            user, existing_oauth_account, oauth_account_dict
                        )

            return user

    return _UserManager


async def get_user_manager(
    user_db=Depends(get_user_db), google_oauth_config=Depends(get_google_oauth_config)
) -> UserManager:
    yield create_user_manager_class(google_oauth_config)(user_db)
