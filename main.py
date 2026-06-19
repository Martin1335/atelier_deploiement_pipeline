from functions.data_cleaning import clean_legorafi_dataframe
from functions.scrapper import scrape_legorafi
from functions.fake_news_detection import enrich_with_fake_news_detection
from functions.hdfs_utils import write_dataframe_to_hdfs


def main():
    # ==========================
    # 1. Scraping
    # ==========================
    raw_df = scrape_legorafi(max_pages=2, sleep_time=0.5)

    # Enregistrement dans HDFS(raw)
    write_dataframe_to_hdfs(
        raw_df,
        "raw/articles_raw.csv",
    )

    # ==========================
    # 2. Nettoyage
    # ==========================
    clean_df = clean_legorafi_dataframe(raw_df)

    # Enregistrement dans HDFS(clean)
    write_dataframe_to_hdfs(
        clean_df,
        "clean/articles_clean.csv",
    )

    # ==========================
    # 3. Détection fake news
    # ==========================
    processed_df = enrich_with_fake_news_detection(clean_df)

    # Enregistrement dans HDFS(processed)
    write_dataframe_to_hdfs(
        processed_df,
        "processed/articles_processed.csv",
    )


if __name__ == "__main__":
    main()