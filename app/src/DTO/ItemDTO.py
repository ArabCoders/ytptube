import json
import time
from dataclasses import dataclass, field
import uuid


@dataclass(kw_only=True)
class ItemDTO:
    _id: int = field(default_factory=lambda: str(uuid.uuid4()), init=False)

    error: str = None
    id: str
    title: str
    url: str
    quality: str
    format: str
    folder: str
    status: str = None
    ytdlp_cookies: str = None
    ytdlp_config: dict = field(default_factory=dict)
    output_template: str = None
    timestamp: int = time.time_ns()
    is_live: bool = None

    # yt-dlp injected fields.
    tmpfilename: str = None
    filename: str = None
    total_bytes: int = None
    total_bytes_estimate: int = None
    downloaded_bytes: int = None
    msg: str = None
    percent: int = None
    speed: str = None
    eta: str = None

    def json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
