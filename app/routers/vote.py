from fastapi import APIRouter,HTTPException,Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema,oauth2,models
router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=201)
def vote(vote:schema.Vote,db: Session=Depends(get_db),current_user=Depends(oauth2.get_user)):
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404,detail=f"Post with id {vote.post_id} is not found")
    
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id , models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if(vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=409,detail=f"User {current_user.id} has already voted on the post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message":"Vote Added Succesfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404,detail=f"User {current_user.id} has Not voted on the post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message":"Vote Deleted Succesfully"}