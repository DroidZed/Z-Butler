import lyricsgenius
from lyricsgenius.artist import Artist
from lyricsgenius.song import Song

from config.main import GENIUS_ACCESS_TOKEN


def get_song_data(title: str, artist_name: str):
    genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

    genius.verbose = True  # Turn off status messages
    genius.remove_section_headers = True  # Remove section headers (e.g. [Chorus]) from lyrics when searching
    genius.skip_non_songs = True  # Include hits thought to be non-songs (e.g. track lists)
    genius.excluded_terms = ["(Remix)", "(Live)"]  # Exclude songs with these words in their title

    song, artist = None, None

    artist: Artist = genius.search_artist(f"{artist_name}", max_songs=1, sort="title", include_features=False)

    if artist:
        song: Song = artist.song(f"{title}")

    return artist, song
