
import urllib.parse


from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)


#used for user login authentication, argument for plain will come from user_credentials.password
def verify(plain_password, hashed_password):
    #verify allows us to compare plain + hashed password
    #plain password from user, hashed from DB
    return pwd_context.verify(plain_password, hashed_password)



#generate spotify link using artist and song name parameters, and returns a str url
def generate_spotify_link(song: str, artist: str) -> str:
    if song and artist:
        #encode the song and artist name for URL compatibility
        encoded_song = urllib.parse.quote(song)
        encoded_artist = urllib.parse.quote(artist)

        #spotify link
        spotify_link = f"https://open.spotify.com/search/{encoded_artist}%20{encoded_song}"
        return spotify_link

    return None