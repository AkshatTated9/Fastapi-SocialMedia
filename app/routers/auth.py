from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schema,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    tags=['Login']
)

@router.post('/login',response_model=schema.Token)
def loginuser(user:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    ifuser=db.query(models.User).filter(models.User.email==user.username).first()

    if not ifuser:
        raise HTTPException(status_code=401 ,detail=f"Invalid Credentials")
    
    if not utils.verify(user.password,ifuser.password):
        raise HTTPException(status_code=401 ,detail=f"Invalid Credentials")
    
    token=oauth2.accesstokencreate({"user_id":ifuser.id})
    return{"access_token":token,"token_type":"bearer"}
