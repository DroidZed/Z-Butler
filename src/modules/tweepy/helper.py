# function getToken(id) {
#   return ((Number(id) / 1e15) * Math.PI)
#     .toString(6 ** 2)
#     .replace(/(0+|\.)/g, '')
# }
#


# TODO: implement this !
import math


def get_token(twt_id: str) -> str:
    return (
        str((float(twt_id) / 1e15) * math.pi)
        .to_bytes(6**2, "big")
        .decode()
        .replace("0", "")
        .replace(".", "")
    )


if __name__ == "__main__":
    print(get_token("1808128291515007224"))
