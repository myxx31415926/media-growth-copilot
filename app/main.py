from app.adapters.csv_adapter import CSVAdapter
from app.agents.collector import CollectorAgent
from app.agents.analyzer import AnalyzerAgent


def main():

    adapter = CSVAdapter("data/mock.csv")
    collector = CollectorAgent(adapter)

    result = collector.run()

    print("\n=== INGESTION REPORT ===")
    print("Raw:", result["total_raw"])
    print("Clean:", result["total_clean"])
    print("Duplicates:", result["duplicates"])

    analyzer = AnalyzerAgent(result["data"])
    analysis = analyzer.run()

    print("\n=== TOP VIDEOS (by engagement_rate) ===")
    for v in analysis["top_videos"]:
        print({
            "video_id": v["video_id"],
            "engagement_rate": v["engagement_rate"],
            "likes": v["likes"],
            "comments": v["comments"],
            "shares": v["shares"]
        })


if __name__ == "__main__":
    main()