class AnalyzerAgent:

    def __init__(self, data):
        self.data = data

    def run(self):

        enriched = []

        for item in self.data:

            views = item["views"]
            likes = item["likes"]
            comments = item["comments"]
            shares = item["shares"]

            if views <= 0:
                engagement_rate = 0
                like_ratio = 0
                comment_ratio = 0
                share_ratio = 0
            else:
                engagement_rate = (likes + comments) / views * 100
                like_ratio = likes / views * 100
                comment_ratio = comments / views * 100
                share_ratio = shares / views * 100

            duration_seconds = item.get("duration_seconds", 0)
            video_url = item.get("video_url") or ""

            enriched_item = item.copy()
            enriched_item.update({
                "engagement_rate": round(engagement_rate, 4),
                "like_ratio": round(like_ratio, 4),
                "comment_ratio": round(comment_ratio, 4),
                "share_ratio": round(share_ratio, 4),
                "is_short": duration_seconds > 0 and duration_seconds <= 60 or "/shorts/" in video_url,
                "content_type": item.get("content_type") or self._content_type(item),
                "product_module": item.get("product_module") or self._product_module(item),
                "product_series": item.get("product_series") or self._product_series(item),
            })

            enriched.append(enriched_item)

        # 排序（最重要）
        top_videos = sorted(
            enriched,
            key=lambda x: x["engagement_rate"],
            reverse=True
        )

        return {
            "enriched": enriched,
            "top_videos": top_videos
        }

    def _content_type(self, item):
        text = self._tag_text(item)

        if "demo" in text:
            return "feature_demo"
        if "review" in text:
            return "review"
        if "tutorial" in text or "how to" in text:
            return "tutorial"
        if "story" in text:
            return "story"
        if "lifestyle" in text:
            return "lifestyle"

        return "entertainment"

    def _product_module(self, item):
        text = self._tag_text(item)

        if "mower" in text or "mow" in text:
            return "割草"
        if "snow" in text:
            return "吹雪"
        if "trimmer" in text or "edge" in text:
            return "修边"
        if "blower" in text or "leaf" in text:
            return "吹叶"
        if "bag" in text or "collect" in text:
            return "集草"
        if "multi" in text:
            return "多模块"
        if "brand" in text:
            return "品牌"

        return "主机"

    def _product_series(self, item):
        text = self._tag_text(item)

        has_m = "m series" in text or "m-series" in text
        has_y = "y series" in text or "y-series" in text

        if has_m and has_y:
            return "mixed"
        if has_m:
            return "M"
        if has_y:
            return "Y"

        return "none"

    def _tag_text(self, item):
        return f"{item.get('title', '')} {item.get('description', '')}".lower()
