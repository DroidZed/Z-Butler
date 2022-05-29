class TweetModel:
    """
    A simple model class to wrap the data received by querying the Twitter API.
    """

    __slots__ = ["__t_id", "__text", "__err"]

    def __init__(self, t_id: str = "", text: str = "", err=""):
        self.__t_id: int = t_id
        self.__text: str = text
        self.__err: str = err

    @property
    def t_id(self):
        return self.__t_id

    @property
    def text(self):
        return self.__text

    @property
    def err(self):
        return self.__err

    @t_id.setter
    def t_id(self, t_id: str):
        self.__t_id = t_id

    @text.setter
    def text(self, text: str):
        self.__text = text

    @err.setter
    def err(self, err: str):
        self.__err = err

    def __dict__(self):
        return {"id": self.t_id, "text": self.__text}

    def __str__(self):
        return "tweet:{'id': '" + self.t_id + "', 'text': '" + self.text + "'}"

    def __repr__(self):
        return "tweet:{'id': '" + self.t_id + "', 'text': '" + self.text + "'}"
