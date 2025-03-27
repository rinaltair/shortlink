from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException


async def toForm(request: Request):
    content_type = request.headers.get("Content-Type")
    if content_type == "application/x-www-form-urlencoded":
        data = await request.form()
        return OAuth2PasswordRequestForm(
            username=data.get("username"),
            password=data.get("password"),
            scope="",
        )

    elif content_type == "application/json":
        json = await request.json()
        return OAuth2PasswordRequestForm(
            username=json.get("username"),
            password=json.get("password"),
            scope="",
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid Content-Type")
