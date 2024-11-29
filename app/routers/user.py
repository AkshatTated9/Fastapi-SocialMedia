from fastapi import HTTPException,Depends,APIRouter
from ..database import get_db
from .. import schema,utils,models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router=APIRouter(
    prefix="/user",
    tags=['User']
)
@router.post("/",status_code=201,response_model=schema.Returnuser)
def createuser(user:schema.Usercreate,db:Session=Depends(get_db)):
    try:
        # Hash the password
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        
        # Create a new user instance
        new_user = models.User(**user.dict())
        
        # Add to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    
    
    return new_user
    
@router.get("/{id}",response_model=schema.Returnuser)
def finduserdetail(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id)
    foundeduser=user.first()
    if not foundeduser:
        raise HTTPException(status_code=404 ,detail=f"User with id:{id} is not found")
    return foundeduser