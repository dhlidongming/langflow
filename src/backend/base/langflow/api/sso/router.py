import uuid

from casdoor import CasdoorSDK
from fastapi import APIRouter, Depends, Form, Response
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, HTTPException
import urllib.parse
import json
from cas import CASClient

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from langflow.services.auth.utils import (
    authenticate_user,
    create_refresh_token,
    create_user_longterm_token,
    create_user_tokens,
    get_user_by_username,
    verify_password,
    get_password_hash,
)
from langflow.services.database.models.folder.utils import create_default_folder_if_it_doesnt_exist
from langflow.services.deps import get_session, get_settings_service, get_variable_service
from langflow.services.settings.service import SettingsService
from langflow.services.variable.service import VariableService

router = APIRouter(tags=["SSO"])
# templates = Jinja2Templates(directory="templates")  # 请确保已经创建了“templates”文件夹并包含“index.html”

async def get_user_from_session(request: Request):
    user = request.session.get("casdoorUser")
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


def get_user_from_db(username: str, password: str, db: Session = Depends(get_session)):
    user = get_user_by_username(db, username)

    if not user:
        # 如果用户不存在，新建用户
        from langflow.services.database.models.user import User, UserCreate
        user = UserCreate(username=username, password=password)
        new_user = User.model_validate(user, from_attributes=True)
        try:
            new_user.password = get_password_hash(user.password)
            new_user.is_active = True
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            folder = create_default_folder_if_it_doesnt_exist(db, new_user.id)
            if not folder:
                raise HTTPException(status_code=500, detail="Error creating default folder")
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="This username is unavailable.") from e
        user = get_user_by_username(db, username)

    if not user.is_active:
        if not user.last_login_at:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Waiting for approval")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

    return user


@router.post("/signin", response_class=JSONResponse)
async def post_signin(response: Response, request: Request,
                      db: Session = Depends(get_session),
                      settings_service=Depends(get_settings_service),
                      variable_service: VariableService = Depends(get_variable_service)):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    sdk = request.app.state.CASDOOR_SDK
    token = sdk.get_oauth_token(code)
    user = sdk.parse_jwt_token(token['access_token'])
    # request.session["casdoorUser"] = user

    try:
        user = get_user_from_db(user['name'], user['id'], db)
    except Exception as exc:
        if isinstance(exc, HTTPException):
            raise exc
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    if user:
        auth_settings = settings_service.auth_settings
        tokens = create_user_tokens(user_id=user.id, db=db, update_last_login=True)
        response.set_cookie(
            "refresh_token_lf",
            tokens["refresh_token"],
            httponly=auth_settings.REFRESH_HTTPONLY,
            samesite=auth_settings.REFRESH_SAME_SITE,
            secure=auth_settings.REFRESH_SECURE,
            expires=auth_settings.REFRESH_TOKEN_EXPIRE_SECONDS,
            domain=auth_settings.COOKIE_DOMAIN,
        )
        response.set_cookie(
            "access_token_lf",
            tokens["access_token"],
            httponly=auth_settings.ACCESS_HTTPONLY,
            samesite=auth_settings.ACCESS_SAME_SITE,
            secure=auth_settings.ACCESS_SECURE,
            expires=auth_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            domain=auth_settings.COOKIE_DOMAIN,
        )
        response.set_cookie(
            "apikey_tkn_lflw",
            str(user.store_api_key),
            httponly=auth_settings.ACCESS_HTTPONLY,
            samesite=auth_settings.ACCESS_SAME_SITE,
            secure=auth_settings.ACCESS_SECURE,
            expires=None,  # Set to None to make it a session cookie
            domain=auth_settings.COOKIE_DOMAIN,
        )
        variable_service.initialize_user_variables(user.id, db)
        # Create default folder for user if it doesn't exist
        create_default_folder_if_it_doesnt_exist(db, user.id)
        return {"status": "ok", "data": tokens}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/login", response_class=JSONResponse)
async def post_signin_cas(response: Response, request: Request,
                      db: Session = Depends(get_session),
                      settings_service=Depends(get_settings_service),
                      variable_service: VariableService = Depends(get_variable_service)):
    ticket = request.query_params.get("ticket")

    cas_client = request.app.state.cas_client
    user, attributes, pgtiou = cas_client.verify_ticket(ticket)
    if not user:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail='Failed to verify ticket.')

    try:
        user = get_user_from_db(user, str(uuid.uuid4()), db)
    except Exception as exc:
        if isinstance(exc, HTTPException):
            raise exc
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    if user:
        auth_settings = settings_service.auth_settings
        tokens = create_user_tokens(user_id=user.id, db=db, update_last_login=True)
        response.set_cookie(
            "refresh_token_lf",
            tokens["refresh_token"],
            httponly=auth_settings.REFRESH_HTTPONLY,
            samesite=auth_settings.REFRESH_SAME_SITE,
            secure=auth_settings.REFRESH_SECURE,
            expires=auth_settings.REFRESH_TOKEN_EXPIRE_SECONDS,
            domain=auth_settings.COOKIE_DOMAIN,
        )
        response.set_cookie(
            "access_token_lf",
            tokens["access_token"],
            httponly=auth_settings.ACCESS_HTTPONLY,
            samesite=auth_settings.ACCESS_SAME_SITE,
            secure=auth_settings.ACCESS_SECURE,
            expires=auth_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            domain=auth_settings.COOKIE_DOMAIN,
        )
        response.set_cookie(
            "apikey_tkn_lflw",
            str(user.store_api_key),
            httponly=auth_settings.ACCESS_HTTPONLY,
            samesite=auth_settings.ACCESS_SAME_SITE,
            secure=auth_settings.ACCESS_SECURE,
            expires=None,  # Set to None to make it a session cookie
            domain=auth_settings.COOKIE_DOMAIN,
        )
        variable_service.initialize_user_variables(user.id, db)
        # Create default folder for user if it doesn't exist
        create_default_folder_if_it_doesnt_exist(db, user.id)
        return {"status": "ok", "data": tokens}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

