from functions.genius import get_song_data


def look_for_song(title: str, artist: str) -> dict:
    artist, song = get_song_data(title, artist)

    if artist and song:

        return {
            "title": title,
            "artist": artist,
            "art_url": song.song_art_image_url,
            "song_url": song.url,
            "valid": True
        }

    else:
        return {
            "valid": False,
        }
