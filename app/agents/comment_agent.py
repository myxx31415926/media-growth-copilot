class CommentAgent:

    def __init__(self, data):
        self.data = data

    def run(self):

        results = []

        for item in self.data:

            text = item.get("text", "").lower()

            sentiment = self._sentiment(text)
            category = self._category(text)
            reply = self._reply_suggestion(sentiment, category)

            results.append({
                "comment_id": item.get("comment_id"),
                "text": item.get("text"),
                "sentiment": sentiment,
                "category": category,
                "reply_suggestion": reply,

                # 🧠 HUMAN-IN-THE-LOOP GATE（关键新增）
                "review_status": "pending_human_review",
                "action_allowed": False
            })

        return results

    # -------------------------
    # sentiment analysis
    # -------------------------
    def _sentiment(self, text):

        if any(w in text for w in ["good", "great", "love", "amazing"]):
            return "positive"

        if any(w in text for w in ["bad", "hate", "terrible", "worst"]):
            return "negative"

        return "neutral"

    # -------------------------
    # category detection
    # -------------------------
    def _category(self, text):

        if "buy" in text or "price" in text:
            return "sales_inquiry"

        if "http" in text or "www" in text:
            return "spam"

        return "normal"

    # -------------------------
    # reply suggestion
    # -------------------------
    def _reply_suggestion(self, sentiment, category):

        if category == "spam":
            return "ignore or remove"

        if category == "sales_inquiry":
            return "provide product details"

        if sentiment == "positive":
            return "thank user"

        if sentiment == "negative":
            return "apologize and assist"

        return "acknowledge"