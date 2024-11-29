from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from . import schema,database,models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "timepass"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

def accesstokencreate(data: dict):
    toencode = data.copy()
    expirytime = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    toencode.update({"exp": expirytime})
    encodedcontent = jwt.encode(toencode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedcontent

def verifyacesstoken(token: str, credential_exception):
    try:
        print("Token received:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:                       
            raise credential_exception
        token_data=schema.Returntoken(id=id)
    except JWTError:
        raise credential_exception
    return token_data

def get_user(token: str = Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credential_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    current_userid=verifyacesstoken(token, credential_exception)
    current_user=db.query(models.User).filter(models.User.id==current_userid.id).first()
    return current_user
