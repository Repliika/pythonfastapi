from fastapi import FastAPI
import psycopg2
from database import engine
from routers import music, users, auth, vote
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# This .py uses psycopg2 to allow us to create a connection to DB
# psycopg2 is a client side cursor that allows us to perform queries client side
# client side frees up performance issues on server. 
# Using a DB frees up saving all posts being loaded in memory



#how you create all the models, so we can use the DB
# models.Music.metadata.create_all(bind=engine)
# models.User.metadata.create_all(bind=engine)
# models.Vote.metadata.create_all(bind=engine)
app = FastAPI()

# * means all
origins = ["*"]
#function that runs before every request, performs an operation
#you allow origins allowed, and methods/ headers etc
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to your postgres DB
try: 
    conn = psycopg2.connect(dbname='fastapi', user='postgres', password='password123')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    print("DB connection successful")
except Exception as error:
    print("DB connection FAILED")
    print("Error: ", error)



app.include_router(music.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


#decorator, this + function turns it into a path operation, if you want to use API hit this endpoint. Attach a method to it. 
# FastAPIapp.HTTPmethod.("path")
#function, async optional if you care for function operating asynchronously.   
@app.get("/")
def root():
    # Choose a random song from the music posts list
    return {"welcome to my music blog!"}








