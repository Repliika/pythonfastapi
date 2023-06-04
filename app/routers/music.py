from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from database import get_db
from sqlalchemy.orm import Session
import schemas, models, utils, oauth2


router = APIRouter(
    tags=['Music']
)


#get all the music posts
@router.get("/music", response_model=List[schemas.Post_Base]) #list the schema to return all
#allow user to search parameters limit, skip and search by string to find certain posts.
def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int = 0):

    # Retrieve all music posts from the database
    all_posts = db.query(models.Music).limit(limit).offset(skip).all()

    post_list = [schemas.Post_Base.from_orm(post) for post in all_posts]
    return post_list
   



#iterate through my_posts to see if query matches parameters a json object is returned 
@router.get("/post/{id}", response_model=schemas.Post_Base)
def find(id: int, db: Session = Depends(get_db)):
    found_post = db.query(models.Music).filter(models.Music.id == id).first()
    if found_post:
        return found_post
    if found_post:
        return {"post": found_post}
    else:
        return {"message": "Post not found"}




#info saving path
@router.get("/info")
def get_info():
    return ("saving for future important text")


#create post
@router.post("/create", status_code=status.HTTP_201_CREATED)
#added dependency of get_current_user which will call verify_access_token and make sure right user is logged in
#returns the user_id in token_data, and we are turning it into an int
def create_post(post: schemas.Create_Post, db: Session = Depends(get_db), 
                user_id: int = Depends(oauth2.get_current_user)):
    print("User ID:", user_id)
    #execute SQL query to insert data from post request that is validated via Post_Base class
    new_post = models.Music(
        song=post.song, artist=post.artist, genre=post.genre, opinion=post.opinion, spotify=post.spotify,  user_id=user_id
    )
    if post.song:
        spotify_link = utils.generate_spotify_link(new_post.song, new_post.artist)
        new_post.spotify = spotify_link           
    else:
        return {"message": "Song does not exist on Spotify"}
    

    
    #need add and commit to say hey i want to add something and run the query.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #store the post inside new_post so we can see in response

    #create a response instance with the required fields
    response = schemas.PostCreate(
        id=new_post.id,
        song=new_post.song,
        artist=new_post.artist,
        genre=new_post.genre,
        opinion=new_post.opinion,
        created_at=new_post.created_at,
        user_id=new_post.user_id
    )
   
    return {"data": response}


#DELETE post via id
@router.delete("/delete/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    #execute SQL query
    post = db.query(models.Music).filter(models.Music.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post does not exist")
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'not authorized')

    db.delete(post)
    db.commit()

        
    return {"message": "Post deleted", "deleted_post": post}




#Search post by ID
#Update only opinion and allowing opinion field, return the whole post
@router.put("/update/{id}", response_model=schemas.Post_Base)
def edit_opinion(id: int, updated_opinion: schemas.UpdateOpinion, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    # Retrieve the post based on the provided id
    post = db.query(models.Music).filter(models.Music.id == id).first()

    if post:
        # Update the opinion field of the post
        post.opinion = updated_opinion.opinion
        db.commit()
        db.refresh(post)
        return post
       
    
