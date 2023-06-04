from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import schemas, database, models, oauth2


router = APIRouter(
    tags=['Vote']
)

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user)
    #need 2 checks for not allowing double votes
    found_vote = vote_query.first()
    if (vote.direction == 1):
        if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'you already voted')
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()
        return{"message": "added vote"}
    else:
        if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'vote does not exist')
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "deleted vote"}


