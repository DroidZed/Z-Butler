# function getToken(id) {
#   return ((Number(id) / 1e15) * Math.PI)
#     .toString(6 ** 2)
#     .replace(/(0+|\.)/g, '')
# }
#

import math
from baseconvert import base


def get_token(twt_id: str) -> str:
    transformation: float = float(twt_id) / 1e15 * math.pi
    result: str = base(str(transformation), 10, 6**2, 1, string=True)  # type:ignore
    return result.replace(".", "").lower()


if __name__ == "__main__":
    print(get_token("1808128291515007224"))
