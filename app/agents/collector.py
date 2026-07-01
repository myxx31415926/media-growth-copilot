class CollectorAgent:

    def __init__(self, adapter):
        self.adapter = adapter

    def run(self):

        raw = self.adapter.fetch()

        cleaned = []
        seen = set()
        duplicates = 0

        for item in raw:
            vid = item["video_id"]

            if vid in seen:
                duplicates += 1
                continue

            seen.add(vid)

            cleaned.append({
                "video_id": vid,
                "title": item["title"],
                "platform": item["platform"],
                "views": int(item["views"]),
                "likes": int(item["likes"]),
                "comments": int(item["comments"]),
                "shares": int(item["shares"]),
                "created_at": item["created_at"]
            })

        return {
            "total_raw": len(raw),
            "total_clean": len(cleaned),
            "duplicates": duplicates,
            "data": cleaned
        }