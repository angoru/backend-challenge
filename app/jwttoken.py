from jose import jwt, exceptions
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


async def get_token_header(request: Request):
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split()
    if len(header_parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = header_parts[1]
    return token


async def jwt_token_verification(request: Request, call_next):
    token = await get_token_header(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.JWSSignatureError:
        return JSONResponse(
            content={"message": "Invalid token signature"}, status_code=401
        )
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token has expired"}, status_code=401)
    except exceptions.JWTError:
        return JSONResponse(content={"message": "Invalid token"}, status_code=401)
    response = await call_next(request)
    return response
