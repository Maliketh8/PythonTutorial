from fastapi import Response, status, HTTPException, APIRouter
from typing import List
from .. import schemas, database

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/", response_model=List[schemas.PostResponse])
def get_user():
    database.cursor.execute("""SELECT * FROM posts""")
    posts = database.cursor.fetchall()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #default status code
def create_posts(new_post: schemas.PostCreate):  #validates data as per schema and puts it in Post schema's format
    database.cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING *""", 
    (new_post.title, new_post.content, new_post.published))
    post = database.cursor.fetchone()
    database.conn.commit() #pushes the above staged changes in DB
    #print(new_post.model_dump()) #converts the Model to dictionary.
    return post

@router.get("/{id}", response_model=schemas.PostResponse) #{id} path parameter 
def get_post(id: int, response: Response): #first validates is id string can be converted to integer then converts it to int.
    database.cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = database.cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") #this looks cleaner than below code
        #response.status_code = 404 #gives 404 error
        #response.status_code = status.HTTP_404_NOT_FOUND #status helps tell which code is for what
        #return {'message' : f"post with id: {id} was not found"}
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    database.cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = database.cursor.fetchone()
    database.conn.commit()
    if deleted_post==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist.")
    
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate):

    database.cursor.execute("""UPDATE posts SET title = %s, content =%s, published = %s WHERE id = %s RETURNING *""",
                   (post.title,post.content,post.published, str(id),))
    
    updated_post = database.cursor.fetchone()
    database.conn.commit()
    if updated_post==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist.")
    return updated_post

