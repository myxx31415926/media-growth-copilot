from datetime import datetime, timezone
import json
import os
from pathlib import Path

from app.adapters.agent_browser_adapter import AgentBrowserAdapter
from app.adapters.csv_adapter import CSVAdapter
from app.agents.collector import CollectorAgent
from app.agents.analyzer import AnalyzerAgent
from app.agents.predictor import PredictorAgent
from app.services.feishu_service import FeishuService
from app.services.feishu_panel_formatter import FeishuPanelFormatter
from app.services.observability_service import ObservabilityService
from app.services.insight_service import InsightService
from app.agents.comment_agent import CommentAgent


def load_env(path=".env"):
    env_path = Path(path)

    if not env_path.exists():
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def build_adapter():
    browser_mock_path = Path("data/agent_browser_mock.json")

    if browser_mock_path.exists():
        return AgentBrowserAdapter(str(browser_mock_path))

    return CSVAdapter("data/mock.csv", "data/mock_comments.csv")


def run_comments(comment_data):

    agent = CommentAgent(comment_data)
    return agent.run()


def build_alert(video):
    return {
        "triggered_at": datetime.now(timezone.utc).isoformat(),
        "alert_type": "viral_signal",
        "alert_message": f"{video['title']} reached {video['viral_score']} viral score.",
        "priority": "high" if video["label"] == "breakout" else "medium",
        "video_url": video.get("video_url"),
    }


def write_dashboard_data(panel):
    dashboard_dir = Path("dashboard")
    dashboard_dir.mkdir(exist_ok=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "media-growth-copilot",
        "tables": panel,
    }

    with open(dashboard_dir / "dashboard_data.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main():
    load_env()

    # -------------------------
    # 1. Data Collection
    # -------------------------
    adapter = build_adapter()
    collector = CollectorAgent(adapter)
    result = collector.run()
    comment_result = collector.run_comments()

    # -------------------------
    # 2. Analysis Layer
    # -------------------------
    analyzer = AnalyzerAgent(result["data"])
    analysis = analyzer.run()

    # -------------------------
    # 3. Prediction Layer
    # -------------------------
    predictor = PredictorAgent(analysis["enriched"])
    predicted = predictor.run()

    # -------------------------
    # 4. Action Layer
    # -------------------------
    feishu = FeishuService(
        provider=os.getenv("FEISHU_PROVIDER", "mock"),
        dashboard_url=os.getenv("DASHBOARD_URL"),
    )
    sent_alerts = []

    print("\n=== VIRAL PREDICTIONS ===")

    for v in predicted:

        print({
            "video_id": v["video_id"],
            "engagement_rate": v["engagement_rate"],
            "viral_score": v["viral_score"],
            "label": v["label"]
        })

        if feishu.send_alert(v):
            sent_alerts.append(build_alert(v))

    # -------------------------
    # 5. Comment Intelligence (Sprint 5)
    # -------------------------
    comment_results = run_comments(comment_result["data"])

    print("\n=== COMMENT INTELLIGENCE ===")

    for r in comment_results:
        print(r)

    # -------------------------
    # 6. Feishu Panel Rows
    # -------------------------
    panel = FeishuPanelFormatter().build(predicted, comment_results, sent_alerts)
    write_dashboard_data(panel)

    print("\n=== FEISHU PANEL TABLES ===")

    for table_name, rows in panel.items():
        print({
            "table": table_name,
            "rows": len(rows)
        })

    # -------------------------
    # 7. Observability Layer (Sprint 6)
    # -------------------------
    obs = ObservabilityService()

    obs.log_videos(predicted)
    obs.log_comments(comment_results)
    obs.generate_report()

    # -------------------------
    # 8. Insight Layer (Sprint 7)
    # -------------------------
    insight = InsightService()
    insight.generate(obs.video_stats, obs.comment_stats)


if __name__ == "__main__":
    main()
