import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from .base import BaseAdapter


class AgentBrowserAdapter(BaseAdapter):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.payload = None

    def fetch(self) -> List[Dict[str, Any]]:
        payload = self._load_payload()
        videos = payload.get("videos", payload if isinstance(payload, list) else [])

        return [self._normalize_video(item) for item in videos]

    def fetch_comments(self) -> List[Dict[str, Any]]:
        payload = self._load_payload()
        comments = payload.get("comments", [])

        return [self._normalize_comment(item) for item in comments]

    def _load_payload(self) -> Any:
        if self.payload is None:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.payload = json.load(f)

        return self.payload

    def _normalize_video(self, item: Dict[str, Any]) -> Dict[str, Any]:
        publish_time = item.get("publish_time") or self._relative_time_to_date(
            item.get("published_relative_time")
        )
        comments_count = self._to_int(item.get("comments_count", item.get("comments", 0)))

        return {
            "video_id": item.get("video_id"),
            "video_url": item.get("video_url"),
            "title": item.get("title"),
            "platform": item.get("platform", "YouTube"),
            "channel_name": item.get("channel_name"),
            "channel_id": item.get("channel_id"),
            "publish_time": publish_time,
            "published_relative_time": item.get("published_relative_time"),
            "views": self._to_int(item.get("views", 0)),
            "thumbnail_url": item.get("thumbnail_url"),
            "duration": item.get("duration"),
            "duration_seconds": self._duration_to_seconds(
                item.get("duration_seconds", item.get("duration"))
            ),
            "description": item.get("description"),
            "likes": self._to_int(item.get("likes", 0)),
            "comments": comments_count,
            "comments_count": comments_count,
            "shares": self._to_int(item.get("shares", 0)),
            "created_at": publish_time,
        }

    def _normalize_comment(self, item: Dict[str, Any]) -> Dict[str, Any]:
        publish_time = item.get("comment_publish_time") or self._relative_time_to_date(
            item.get("comment_published_relative_time")
        )

        return {
            "comment_id": item.get("comment_id"),
            "video_id": item.get("video_id"),
            "video_url": item.get("video_url"),
            "text": item.get("comment_content", item.get("text", "")),
            "comment_content": item.get("comment_content", item.get("text", "")),
            "comment_author": item.get("comment_author"),
            "likes_count": self._to_int(
                item.get("comment_likes_count", item.get("likes_count", 0))
            ),
            "comment_publish_time": publish_time,
            "comment_published_relative_time": item.get(
                "comment_published_relative_time"
            ),
        }

    def _to_int(self, value: Any) -> int:
        if value in (None, ""):
            return 0

        if isinstance(value, (int, float)):
            return int(value)

        text = str(value).strip().replace(",", "")
        match = re.match(r"^(\d+(?:\.\d+)?)([KkMm])?$", text)

        if not match:
            digits = re.sub(r"[^\d.]", "", text)
            return int(float(digits)) if digits else 0

        number = float(match.group(1))
        suffix = match.group(2)

        if suffix and suffix.lower() == "k":
            number *= 1_000
        elif suffix and suffix.lower() == "m":
            number *= 1_000_000

        return int(number)

    def _duration_to_seconds(self, value: Any) -> int:
        if value in (None, ""):
            return 0

        if isinstance(value, (int, float)):
            return int(value)

        parts = [int(part) for part in str(value).split(":") if part.isdigit()]

        if len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]

        if len(parts) == 2:
            return parts[0] * 60 + parts[1]

        if len(parts) == 1:
            return parts[0]

        return 0

    def _relative_time_to_date(self, value: Any) -> str:
        if not value:
            return ""

        text = str(value).lower()
        match = re.search(r"(\d+)\s+(minute|hour|day|week|month|year)s?\s+ago", text)

        if not match:
            return str(value)

        amount = int(match.group(1))
        unit = match.group(2)
        now = datetime.now(timezone.utc)

        if unit == "minute":
            delta = timedelta(minutes=amount)
        elif unit == "hour":
            delta = timedelta(hours=amount)
        elif unit == "day":
            delta = timedelta(days=amount)
        elif unit == "week":
            delta = timedelta(weeks=amount)
        elif unit == "month":
            delta = timedelta(days=amount * 30)
        else:
            delta = timedelta(days=amount * 365)

        return (now - delta).date().isoformat()
