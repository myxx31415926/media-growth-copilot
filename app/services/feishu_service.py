import json
import os
import urllib.error
import urllib.request


class FeishuService:

    def __init__(self, provider="mock", dashboard_url=None):
        self.provider = provider
        self.dashboard_url = dashboard_url or os.getenv("DASHBOARD_URL", "")
        self.sent = set()  # deduplication

    def send_alert(self, video):

        video_id = video["video_id"]

        # -------------------------
        # deduplication
        # -------------------------
        if video_id in self.sent:
            return False

        # -------------------------
        # trigger condition
        # -------------------------
        if video["label"] not in ["high", "breakout"]:
            return False

        message = self._format_message(video)

        if self.provider == "mock":
            self._mock_send(message)
        else:
            if not self._real_send(message):
                return False

        self.sent.add(video_id)
        return True

    def _format_message(self, video):

        return {
            "title": "🚨 Viral Content Alert",
            "video_id": video["video_id"],
            "video_title": video.get("title"),
            "video_url": video.get("video_url"),
            "viral_score": video["viral_score"],
            "label": video["label"],
            "engagement_rate": video.get("engagement_rate"),
            "dashboard_url": self.dashboard_url,
        }

    def _mock_send(self, message):
        print("\n[FEISHU MOCK ALERT]")
        print(message)

    def _real_send(self, message):
        webhook_url = os.getenv("FEISHU_WEBHOOK_URL")

        if self.provider == "webhook":
            if not webhook_url:
                print("[FEISHU ERROR] Missing FEISHU_WEBHOOK_URL.")
                return False

            return self._send_webhook_card(webhook_url, message)

        if webhook_url:
            return self._send_webhook_card(webhook_url, message)

        return self._send_app_message(message)

    def _send_webhook_card(self, webhook_url, message):
        payload = {
            "msg_type": "interactive",
            "card": self._build_card(message),
        }

        response = self._post_json(webhook_url, payload)
        return response is not None

    def _send_app_message(self, message):
        receive_id = os.getenv("FEISHU_RECEIVE_ID")
        receive_id_type = os.getenv("FEISHU_RECEIVE_ID_TYPE", "chat_id")

        if not receive_id:
            print("[FEISHU ERROR] Missing FEISHU_RECEIVE_ID.")
            return False

        token = self._tenant_access_token()

        if not token:
            return False

        url = (
            "https://open.feishu.cn/open-apis/im/v1/messages"
            f"?receive_id_type={receive_id_type}"
        )
        payload = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json.dumps(self._build_card(message), ensure_ascii=False),
        }
        headers = {"Authorization": f"Bearer {token}"}

        response = self._post_json(url, payload, headers=headers)
        return response is not None

    def _tenant_access_token(self):
        app_id = os.getenv("FEISHU_APP_ID")
        app_secret = os.getenv("FEISHU_APP_SECRET")

        if not app_id or not app_secret:
            print("[FEISHU ERROR] Missing FEISHU_APP_ID or FEISHU_APP_SECRET.")
            return None

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        response = self._post_json(url, {
            "app_id": app_id,
            "app_secret": app_secret,
        })

        if not response:
            return None

        token = response.get("tenant_access_token")

        if not token:
            print(f"[FEISHU ERROR] Token response missing tenant_access_token: {response}")

        return token

    def _build_card(self, message):
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        f"**{message.get('video_title') or message['video_id']}**\n"
                        f"Viral Score: **{message['viral_score']}**\n"
                        f"Engagement Rate: **{message.get('engagement_rate')}%**\n"
                        f"Tier: **{message['label']}**"
                    ),
                },
            }
        ]

        actions = []

        if message.get("dashboard_url"):
            actions.append({
                "tag": "button",
                "text": {"tag": "plain_text", "content": "查看数据面板"},
                "type": "primary",
                "url": message["dashboard_url"],
            })

        if message.get("video_url"):
            actions.append({
                "tag": "button",
                "text": {"tag": "plain_text", "content": "打开视频"},
                "url": message["video_url"],
            })

        if actions:
            elements.append({"tag": "action", "actions": actions})

        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "template": "green",
                "title": {"tag": "plain_text", "content": message["title"]},
            },
            "elements": elements,
        }

    def _post_json(self, url, payload, headers=None):
        request_headers = {
            "Content-Type": "application/json; charset=utf-8",
        }

        if headers:
            request_headers.update(headers)

        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=request_headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8")
            print(f"[FEISHU ERROR] HTTP {error.code}: {body}")
            return None
        except urllib.error.URLError as error:
            print(f"[FEISHU ERROR] Network error: {error}")
            return None

        if not body:
            return {}

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            print(f"[FEISHU ERROR] Non-JSON response: {body}")
            return None

        if data.get("code", 0) != 0:
            print(f"[FEISHU ERROR] API response: {data}")
            return None

        return data
