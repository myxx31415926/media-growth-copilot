from datetime import datetime, timezone


class FeishuPanelFormatter:
    def build(self, videos, comments, sent_alerts):
        return {
            "performance_overview": self._performance_overview(videos),
            "trend_snapshot": self._trend_snapshot(videos),
            "viral_tracking": self._viral_tracking(videos, comments),
            "comments_pending": self._comments_pending(comments),
            "alert_history": self._alert_history(sent_alerts),
        }

    def _performance_overview(self, videos):
        rows = []

        for video in videos:
            rows.append({
                "thumbnail_url": video.get("thumbnail_url"),
                "title": video.get("title"),
                "video_url": video.get("video_url"),
                "views": video.get("views"),
                "likes": video.get("likes"),
                "comments_count": video.get("comments_count", video.get("comments")),
                "engagement_rate": video.get("engagement_rate"),
                "comment_rate": video.get("comment_ratio"),
                "is_short": video.get("is_short"),
                "content_type": video.get("content_type"),
                "product_module": video.get("product_module"),
                "product_series": video.get("product_series"),
                "publish_time": video.get("publish_time"),
                "viral_score": video.get("viral_score"),
            })

        return sorted(rows, key=lambda row: row.get("viral_score") or 0, reverse=True)

    def _trend_snapshot(self, videos):
        snapshot_at = datetime.now(timezone.utc).date().isoformat()
        rows = []

        for video in videos:
            rows.append({
                "thumbnail_url": video.get("thumbnail_url"),
                "title": video.get("title"),
                "video_url": video.get("video_url"),
                "snapshot_at": snapshot_at,
                "views": video.get("views"),
                "view_delta": video.get("view_delta", 0),
                "view_velocity": video.get("view_velocity", 0),
            })

        return rows

    def _viral_tracking(self, videos, comments):
        positive_ratio_by_url = self._positive_comment_ratio_by_url(comments)
        rows = []

        for video in videos:
            video_url = video.get("video_url")
            rows.append({
                "thumbnail_url": video.get("thumbnail_url"),
                "title": video.get("title"),
                "video_url": video_url,
                "viral_score": video.get("viral_score"),
                "viral_tier": video.get("viral_tier"),
                "view_velocity": video.get("view_velocity", 0),
                "engagement_rate": video.get("engagement_rate"),
                "content_type": video.get("content_type"),
                "product_module": video.get("product_module"),
                "is_short": video.get("is_short"),
                "positive_comment_ratio": positive_ratio_by_url.get(video_url, 0),
            })

        return sorted(rows, key=lambda row: row.get("viral_score") or 0, reverse=True)

    def _comments_pending(self, comments):
        rows = []

        for comment in comments:
            rows.append({
                "comment_content": comment.get("comment_content", comment.get("text")),
                "sentiment": comment.get("sentiment"),
                "category": comment.get("category"),
                "video_url": comment.get("video_url"),
                "likes_count": comment.get("likes_count"),
                "reply_suggestion": comment.get("reply_suggestion"),
                "approval_status": comment.get("approval_status", "pending"),
            })

        return sorted(rows, key=lambda row: row.get("likes_count") or 0, reverse=True)

    def _alert_history(self, sent_alerts):
        rows = []

        for alert in sent_alerts:
            rows.append({
                "triggered_at": alert.get("triggered_at"),
                "alert_type": alert.get("alert_type"),
                "alert_message": alert.get("alert_message"),
                "priority": alert.get("priority"),
                "video_url": alert.get("video_url"),
            })

        return rows

    def _positive_comment_ratio_by_url(self, comments):
        totals = {}
        positives = {}

        for comment in comments:
            video_url = comment.get("video_url")

            if not video_url:
                continue

            totals[video_url] = totals.get(video_url, 0) + 1

            if comment.get("sentiment") == "positive":
                positives[video_url] = positives.get(video_url, 0) + 1

        return {
            video_url: round(positives.get(video_url, 0) / total, 4)
            for video_url, total in totals.items()
        }
