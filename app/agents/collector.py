class CollectorAgent:

    def __init__(self, adapter):
        self.adapter = adapter

    def run(self):

        raw = self.adapter.fetch()

        cleaned = []
        seen = set()
        duplicates = 0

        for item in raw:
            vid = item.get("video_id")

            if not vid:
                continue

            if vid in seen:
                duplicates += 1
                continue

            seen.add(vid)

            cleaned.append({
                "video_id": vid,
                "video_url": item.get("video_url"),
                "title": item.get("title", ""),
                "platform": item.get("platform", "YouTube"),
                "channel_name": item.get("channel_name"),
                "channel_id": item.get("channel_id"),
                "publish_time": item.get("publish_time", item.get("created_at", "")),
                "published_relative_time": item.get("published_relative_time"),
                "views": self._to_int(item.get("views", 0)),
                "thumbnail_url": item.get("thumbnail_url"),
                "duration": item.get("duration"),
                "duration_seconds": self._to_int(item.get("duration_seconds", 0)),
                "description": item.get("description"),
                "likes": self._to_int(item.get("likes", 0)),
                "comments": self._to_int(item.get("comments", item.get("comments_count", 0))),
                "comments_count": self._to_int(item.get("comments_count", item.get("comments", 0))),
                "shares": self._to_int(item.get("shares", 0)),
                "created_at": item.get("created_at", item.get("publish_time", ""))
            })

        return {
            "total_raw": len(raw),
            "total_clean": len(cleaned),
            "duplicates": duplicates,
            "data": cleaned
        }

    def run_comments(self):

        raw = self.adapter.fetch_comments()
        cleaned = []

        for item in raw:
            cleaned.append({
                "comment_id": item.get("comment_id"),
                "video_id": item.get("video_id"),
                "video_url": item.get("video_url"),
                "text": item.get("text", item.get("comment_content", "")),
                "comment_content": item.get("comment_content", item.get("text", "")),
                "comment_author": item.get("comment_author"),
                "likes_count": self._to_int(item.get("likes_count", item.get("comment_likes_count", 0))),
                "comment_publish_time": item.get("comment_publish_time"),
                "comment_published_relative_time": item.get("comment_published_relative_time"),
            })

        return {
            "total_raw": len(raw),
            "total_clean": len(cleaned),
            "data": cleaned
        }

    def _to_int(self, value):
        if value in (None, ""):
            return 0

        return int(value)
