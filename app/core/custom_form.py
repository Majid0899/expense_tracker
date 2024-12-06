from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm

class OAuth2PasswordRequestFormEmail(OAuth2PasswordRequestForm):
    def __init__(
        self,
        email: str = Form(...),  # Use `email` instead of `username`
        password: str = Form(...),
        scope: str = Form(""),
        client_id: str = Form(None),
        client_secret: str = Form(None),
    ):
        super().__init__(
            username=email,  # Map email to username internally
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )


