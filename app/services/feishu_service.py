class FeishuService:

    def __init__(self, provider="mock"):
        self.provider = provider
        self.sent = set()  # deduplication

    def send_alert(self, video):

        video_id = video["video_id"]

        # -------------------------
        # deduplication
        # -------------------------
        if video_id in self.sent:
            return

        # -------------------------
        # trigger condition
        # -------------------------
        if video["label"] not in ["high", "breakout"]:
            return

        message = self._format_message(video)

        if self.provider == "mock":
            self._mock_send(message)
        else:
            self._real_send(message)

        self.sent.add(video_id)

    def _format_message(self, video):

        return {
            "title": "🚨 Viral Content Alert",
            "video_id": video["video_id"],
            "viral_score": video["viral_score"],
            "label": video["label"],
            "engagement_rate": video.get("engagement_rate")
        }

    def _mock_send(self, message):
        print("\n[FEISHU MOCK ALERT]")
        print(message)

    def _real_send(self, message):
        # 公司API接入点（Sprint 4不实现）
        pass