class Album:
    
    def __init__(self, name: str, art: str):
        self.name = name
        self.art = art
        

class Artist:
    
    def __init__(self, name: str):
        self.name = name


class Song:
    
    def __init__(self, name: str, artists: list[Artist], album: Album, href: str):
        
        self.name = name
        self.artists = artists
        self.album = album
        self.href = href


class ClientAuth:
    
    def __init__(self, access_token: str, token_type: str, expires_in: int) -> None:
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in