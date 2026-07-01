from app.adapters.csv_adapter import CSVAdapter
from app.agents.collector import CollectorAgent
from app.agents.analyzer import AnalyzerAgent
from app.agents.predictor import PredictorAgent
from app.services.feishu_service import FeishuService
from app.services.observability_service import ObservabilityService
from app.services.insight_service import InsightService
from app.agents.comment_agent import CommentAgent
import csv


def run_comments():

    comments = []

    with open("data/mock_comments.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            comments.append(row)

    agent = CommentAgent(comments)
    return agent.run()


def main():

    # -------------------------
    # 1. Data Collection
    # -------------------------
    adapter = CSVAdapter("data/mock.csv")
    collector = CollectorAgent(adapter)
    result = collector.run()

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
    feishu = FeishuService(provider="mock")

    print("\n=== VIRAL PREDICTIONS ===")

    for v in predicted:

        print({
            "video_id": v["video_id"],
            "engagement_rate": v["engagement_rate"],
            "viral_score": v["viral_score"],
            "label": v["label"]
        })

        feishu.send_alert(v)

    # -------------------------
    # 5. Comment Intelligence (Sprint 5)
    # -------------------------
    comment_results = run_comments()

    print("\n=== COMMENT INTELLIGENCE ===")

    for r in comment_results:
        print(r)

    # -------------------------
    # 6. Observability Layer (Sprint 6)
    # -------------------------
    obs = ObservabilityService()

    obs.log_videos(predicted)
    obs.log_comments(comment_results)
    obs.generate_report()

    # -------------------------
    # 7. Insight Layer (Sprint 7) ⭐ FINAL PIECE
    # -------------------------
    insight = InsightService()
    insight.generate(obs.video_stats, obs.comment_stats)


if __name__ == "__main__":
    main()