class ObservabilityService:

    def __init__(self):
        self.video_stats = {}
        self.comment_stats = {}

    # -------------------------
    # VIDEO METRICS
    # -------------------------
    def log_videos(self, videos):

        total = len(videos)
        label_count = {"low": 0, "medium": 0, "high": 0, "breakout": 0}

        for v in videos:
            label_count[v["label"]] += 1

        self.video_stats = {
            "total_videos": total,
            "label_distribution": label_count
        }

    # -------------------------
    # COMMENT METRICS
    # -------------------------
    def log_comments(self, comments):

        total = len(comments)

        sentiment_count = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

        category_count = {}

        pending_review = 0

        for c in comments:

            sentiment_count[c["sentiment"]] += 1
            category = c["category"]
            category_count[category] = category_count.get(category, 0) + 1

            if c.get("review_status") == "pending_human_review":
                pending_review += 1

        self.comment_stats = {
            "total_comments": total,
            "sentiment_distribution": sentiment_count,
            "category_distribution": category_count,
            "pending_review": pending_review
        }

    # -------------------------
    # FINAL REPORT
    # -------------------------
    def generate_report(self):

        print("\n========================")
        print("📊 SYSTEM OBSERVABILITY REPORT")
        print("========================")

        print("\n--- VIDEO STATS ---")
        print(self.video_stats)

        print("\n--- COMMENT STATS ---")
        print(self.comment_stats)

        print("\n========================\n")
