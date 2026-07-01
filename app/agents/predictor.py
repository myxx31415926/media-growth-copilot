class PredictorAgent:

    def __init__(self, data):
        self.data = data

    def run(self):

        result = []

        for item in self.data:

            engagement_rate = item.get("engagement_rate", 0)

            views = item["views"]
            likes = item["likes"]
            comments = item["comments"]
            shares = item["shares"]

            # -------------------------
            # scoring model
            # -------------------------
            score = engagement_rate * 500

            if comments > likes * 0.3:
                score += 10

            if views > 1000:
                score += 20

            viral_score = max(0, min(100, round(score, 2)))

            # -------------------------
            # label
            # -------------------------
            if viral_score >= 75:
                label = "breakout"
            elif viral_score >= 50:
                label = "high"
            elif viral_score >= 25:
                label = "medium"
            else:
                label = "low"

            new_item = item.copy()
            new_item.update({
                "viral_score": viral_score,
                "label": label
            })

            result.append(new_item)

        return result