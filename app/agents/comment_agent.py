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
                "video_id": item.get("video_id"),
                "video_url": item.get("video_url"),
                "text": item.get("text"),
                "comment_content": item.get("comment_content", item.get("text")),
                "comment_author": item.get("comment_author"),
                "likes_count": item.get("likes_count", 0),
                "sentiment": sentiment,
                "category": category,
                "reply_suggestion": reply,

                # Human-in-the-loop gate.
                "review_status": "pending_human_review",
                "approval_status": "pending",
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

        if "http" in text or "www" in text:
            return "垃圾"

        if any(w in text for w in ["danger", "unsafe", "scam", "fake"]):
            return "风险"

        if "buy" in text or "price" in text:
            return "询购"

        if any(w in text for w in ["bad", "hate", "terrible", "worst"]):
            return "投诉"

        if "?" in text or any(w in text for w in ["how", "where", "when", "can i"]):
            return "提问"

        if any(w in text for w in ["good", "great", "love", "amazing"]):
            return "夸赞"

        return "提问"

    # -------------------------
    # reply suggestion
    # -------------------------
    def _reply_suggestion(self, sentiment, category):

        if category == "垃圾":
            return "ignore or remove"

        if category == "风险":
            return "escalate for manual review"

        if category == "询购":
            return "provide product details"

        if sentiment == "positive":
            return "thank user"

        if sentiment == "negative":
            return "apologize and assist"

        return "acknowledge"
