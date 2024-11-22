import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify credentials
CLIENT_ID = "a269acb807cb4051ada7c1830c83c0b0"
CLIENT_SECRET = "919ccebaf342400faa377b9eb5ad7621"

def get_spotify_client():
    """Authenticate with Spotify and return a client."""
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_recommendations(emotion):
    """Get song recommendations based on the detected emotion."""
    
    # Mapping the emotions to corresponding genres
    emotion_to_genre = {
        "Angry": "rock",        # Rock for intense, aggressive emotions
        "Disgusted": "metal",   # Metal for disgust, dark themes
        "Fear": "dark ambient", # Dark ambient music for fear
        "Happy": "pop",         # Pop for happy and upbeat vibes
        "Sad": "acoustic",      # Acoustic for sad, mellow moods
        "Surprise": "indie",    # Indie for unexpected and varied moods
        "Neutral": "classical", # Classical for neutral, calm states
    }

    genre = emotion_to_genre.get(emotion, "pop")  # Default to pop if emotion is unknown
    
    # Get Spotify client
    spotify = get_spotify_client()
    
    # Fetch recommendations based on the mapped genre
    results = spotify.recommendations(seed_genres=[genre], limit=10)
    
    # Extract the relevant information about each song
    songs = [
        {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"],
            "album_cover": track["album"]["images"][0]["url"]  # Get the album cover image
        }
        for track in results["tracks"]
    ]
    
    return songs
