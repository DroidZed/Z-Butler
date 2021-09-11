from config.genius import get_song_data


def query_lyrics(title: str, artist: str) -> dict:

    artist, song = get_song_data(title, artist)

    if artist and song:

        return {
            "title": title,
            "artist": artist,
            "art_url": song.song_art_image_url,
            "song_url": song.url,
            "lyrics": song.lyrics,
            "valid": True
        }

    else:
        return {
            "valid": False,
        }
