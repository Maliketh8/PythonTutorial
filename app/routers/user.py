from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/users",
    tags=['Users']
)
 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump()) #it unpacks all the fields so we dont have to type each like in above comment. 
    db.add(new_user) #add new post
    db.commit() #commit it
    db.refresh(new_user) #retrieve newly created post and store it in new_post
    return new_user

@router.get('/{id}', status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() #.first() gives the first matched value instead of looking more in the db

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    
    return user