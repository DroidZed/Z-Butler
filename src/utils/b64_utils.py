from base64 import b64encode, b64decode


def strToB64(s: str):
    return b64encode(s.encode("utf-8"))


def b64ToStr(b: str):
    return b64decode(b).decode("utf-8")
