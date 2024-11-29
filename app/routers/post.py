from fastapi import HTTPException,Depends,APIRouter
from ..database import get_db
from .. import schema,models,oauth2
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)
@router.get("/",response_model=List[schema.Postout])
def getallposts(db: Session=Depends(get_db),limit :int =10,skip: int =0,search:Optional[str]=''):
    # cursor.execute(""" SELECT * from posts""")
    # my_post=cursor.fetchall()
    #my_post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Vote.post_id).label('Votes')).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    return results



# @app.post("/posts")
# def createpost(payLoad: dict=Body(...)):
#     print(payLoad)
#     return{"new Post": f"Title: {payLoad['Title']} Content: {payLoad['Description']}"}

@router.post("/",response_model=schema.Returnpost)
def createpost(npost: schema.Createpost,db: Session=Depends(get_db),current_user = Depends(oauth2.get_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(npost.Title,npost.Description,npost.Published))
    # ans=cursor.fetchone()
    # conn.commit()
    ans=models.Post(owner_id=current_user.id,**npost.dict())
    db.add(ans)
    db.commit()
    db.refresh(ans)
    return ans
    

@router.get("/{id}",response_model=schema.Returnpost)
def get_post(id :int,db: Session=Depends(get_db)):     # This ensures that the param is interger and coverts it from string 
    # cursor.execute(" SELECT * from posts WHERE ID=%s",(str(id)))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=404 ,detail=f"Post with {id} is not found")
    return post

@router.delete("/{id}")
def deletepost(id:int,db:Session=Depends(get_db),current_user  = Depends(oauth2.get_user)):
    # cursor.execute("DELETE  FROM posts WHERE ID=%s RETURNING *",(str(id)))
    # posttobedeleted=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    posttobedeleted=post.first()
    if not posttobedeleted:
        raise HTTPException(status_code=404 ,detail=f"Post with id:{id} is not found")
    if posttobedeleted.owner_id != current_user.id:
        raise HTTPException(status_code=403 ,detail=f"Not authorised to perform particular action")
    post.delete(synchronize_session=False)
    db.commit()
    return{"Deleted"}

@router.put("/{id}",response_model=schema.Returnpost)
def updatepost(id:int,post:schema.Createpost,db:Session=Depends(get_db),current_user  = Depends(oauth2.get_user)):
    # cursor.execute("UPDATE posts SET title=%s , content=%s , published=%s WHERE id=%s RETURNING *",(post.Title,post.Description,post.Published,str(id)))
    # conn.commit()
    # update=cursor.fetchone()
    posttquery=db.query(models.Post).filter(models.Post.id==id)
    updatepost=posttquery.first()
    if not updatepost:
        raise HTTPException(status_code=404 ,detail=f"Post with id:{id} is not found")
    if updatepost.owner_id != current_user.id:
        raise HTTPException(status_code=403 ,detail=f"Not authorised to perform particular action")
    posttquery.update(post.dict(),synchronize_session=False)
    db.commit()
    return posttquery.first()