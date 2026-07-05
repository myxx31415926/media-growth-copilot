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
            score = engagement_rate * 5

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
                viral_tier = "viral"
            elif viral_score >= 50:
                label = "high"
                viral_tier = "rising"
            elif viral_score >= 25:
                label = "medium"
                viral_tier = "seed"
            else:
                label = "low"
                viral_tier = "seed"

            new_item = item.copy()
            new_item.update({
                "viral_score": viral_score,
                "label": label,
                "viral_tier": viral_tier
            })

            result.append(new_item)

        return result
