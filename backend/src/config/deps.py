from fastapi.security import APIKeyCookie, OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request, HTTPException, status
from typing import Optional, Dict

from src.utils.constant import auth

# cookie_scheme = APIKeyCookie(name="access_token", description="API Key")


def predefinedJsonRes(message, data, code=200):
    status = "success" if str(code).startswith("2") else "error"
    return {"message": message, "data": data, "status": status, "code": code}


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        token = request.cookies.get("access_token")
        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=predefinedJsonRes(
                        message=auth["UNAUTHORIZED"],
                        data=None,
                        code=status.HTTP_401_UNAUTHORIZED,
                    ),
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return token


oauth_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/login")
