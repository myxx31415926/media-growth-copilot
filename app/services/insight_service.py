class InsightService:

    def generate(self, video_stats, comment_stats):

        print("\n========================")
        print("🧠 EXECUTIVE INSIGHTS REPORT")
        print("========================")

        # -------------------------
        # 1. WHAT HAPPENED
        # -------------------------
        self._what_happened(video_stats, comment_stats)

        # -------------------------
        # 2. WHY IT HAPPENED
        # -------------------------
        self._why_it_happened(video_stats, comment_stats)

        # -------------------------
        # 3. WHAT TO DO NEXT
        # -------------------------
        self._what_to_do(video_stats, comment_stats)

        print("\n========================\n")

    # -------------------------
    # 1. WHAT HAPPENED
    # -------------------------
    def _what_happened(self, v, c):

        print("\n📊 WHAT HAPPENED")

        total_videos = v["total_videos"]
        label = v["label_distribution"]

        total_comments = c["total_comments"]
        sentiment = c["sentiment_distribution"]

        print(f"- Total videos analyzed: {total_videos}")
        print(f"- Total comments analyzed: {total_comments}")

        print(f"- Video distribution: {label}")
        print(f"- Comment sentiment: {sentiment}")

    # -------------------------
    # 2. WHY IT HAPPENED
    # -------------------------
    def _why_it_happened(self, v, c):

        print("\n🧠 WHY IT HAPPENED")

        high_ratio = 0

        total = v["total_videos"]
        high_ratio = (v["label_distribution"]["high"] + v["label_distribution"]["breakout"]) / total

        if high_ratio > 0.5:
            print("- High viral content ratio is strong due to boosted engagement signals.")
        else:
            print("- Content is mostly mid/low performance, indicating weak engagement signals.")

        if c["category_distribution"].get("垃圾", 0) > 0:
            print("- Spam comments detected, lowering engagement quality signal.")

    # -------------------------
    # 3. WHAT TO DO NEXT
    # -------------------------
    def _what_to_do(self, v, c):

        print("\n📈 WHAT TO DO NEXT")

        if v["label_distribution"]["high"] + v["label_distribution"]["breakout"] > 0:
            print("- Double down on high-performing content formats.")

        if c["sentiment_distribution"]["negative"] > 0:
            print("- Improve comment response strategy for negative sentiment.")

        print("- Optimize content hooks in first 3 seconds.")
        print("- Increase A/B testing on top-performing videos.")
