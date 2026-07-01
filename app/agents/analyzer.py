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

            engagement_rate = (likes + comments + shares) / views

            like_ratio = likes / views
            comment_ratio = comments / views
            share_ratio = shares / views

            enriched_item = item.copy()
            enriched_item.update({
                "engagement_rate": round(engagement_rate, 4),
                "like_ratio": round(like_ratio, 4),
                "comment_ratio": round(comment_ratio, 4),
                "share_ratio": round(share_ratio, 4)
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