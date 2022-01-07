from lyricsgenius import Genius
from lyricsgenius.artist import Artist
from lyricsgenius.song import Song

from config.main import GENIUS_ACCESS_TOKEN


def get_song_data(title: str, artist_name: str) -> tuple[Artist | None, Song | None]:

    """
    A function utilizing the Genius API to fetch a song's data, mainly the lyrics.
    Args:
        title: title of the song.
        artist_name: the full and correct artist name

    Returns:
        A tuple containing a song object and an artist object.
    """

    genius = Genius(GENIUS_ACCESS_TOKEN)

    genius.verbose = True  # Turn off status messages
    genius.remove_section_headers = True  # Remove section headers (e.g. [Chorus]) from lyrics when searching
    genius.skip_non_songs = True  # Include hits thought to be non-songs (e.g. track lists)
    genius.excluded_terms = [
        "(Remix)",
        "(Live)",
    ]  # Exclude songs with these words in their title

    artist, song = None, None

    artist: Artist = genius.search_artist(f"{artist_name}", max_songs=1, sort="title", include_features=False)

    if artist:
        song: Song = artist.song(f"{title}")

    return artist, song
