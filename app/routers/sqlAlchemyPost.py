from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

router = APIRouter(
    prefix="/sqlalchemy",
    tags=['SQLAlchemy Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def test_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), Limit: int = 10, skip: int = 0, search: Optional[str] = ""): #limit is a query parameter with default value 10
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    print(search)
    return posts
#@router.post("/createposts")
#def create_posts(payLoad: dict = Body(...)): It will extract all from body, convert to dictionary and store in var named payLoad
    # print(payLoad)
    # return {"new post" : f"title {payLoad['title']} content: {payLoad['content']}" }


@router.post("/posts", status_code=status.HTTP_201_CREATED) #default status code
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.PostResponse,current_user: int = Depends(oauth2.get_current_user)):  #validates data as per schema and puts it in Post schema's format
    #new_post = models.Post(title=post.title, content=post.content,published=post.published)    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) #it unpacks all the fields so we dont have to type each like in above comment. 
    db.add(new_post) #add new post
    db.commit() #commit it
    db.refresh(new_post) #retrieve newly created post and store it in new_post
    return new_post



@router.get("/posts/{id}", response_model=schemas.PostResponse) #{id} path parameter 
def get_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): #first validates is id string can be converted to integer then converts it to int.
    post = db.query(models.Post).filter(models.Post.id == id).first() #.first() gives the first matched value instead of looking more in the db
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") #this looks cleaner than below code
        #response.status_code = 404 #gives 404 error
        #response.status_code = status.HTTP_404_NOT_FOUND #status helps tell which code is for what
        #return {'message' : f"post with id: {id} was not found"}
    return post
 

@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int,updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(updated_post.model_dump(), synchronize_session=False) #update() of sqlalchemy needs dictionary of values to update.
    db.commit()
    return post_query.first()
