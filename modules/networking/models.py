from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional

from .http_errors import RequestError


@dataclass
class Result:
    Error: Optional[RequestError]
    Data: Optional[Any]
