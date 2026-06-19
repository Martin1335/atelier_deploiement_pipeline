import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep


def scrape_legorafi(max_pages=1, sleep_time=0.1, user_agent="Mozilla/5.0"):
    """
    Scrape les articles du Gorafi et retourne un DataFrame.

    Parameters
    ----------
    max_pages : int
        Nombre de pages de la homepage à scraper (pagination simple).
    sleep_time : float
        Pause entre les requêtes (anti-spam).
    user_agent : str
        User-Agent HTTP.

    Returns
    -------
    pd.DataFrame
        Colonnes : ID, Titre, DatePublication, Contenu, URL
    """

    headers = {"User-Agent": user_agent}

    article_urls = []

    # ==========================
    # Collecte des URLs
    # ==========================
    for page in range(1, max_pages + 1):

        if page == 1:
            url = "https://www.legorafi.fr/"
        else:
            url = f"https://www.legorafi.fr/page/{page}/"

        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        urls = [
            a["href"]
            for a in soup.find_all("a", rel="bookmark")
            if a.get("href")
        ]

        article_urls.extend(urls)
        sleep(sleep_time)

    # Suppression doublons en gardant l'ordre
    article_urls = list(dict.fromkeys(article_urls))

    # ==========================
    # Scraping articles
    # ==========================
    rows = []

    for idx, url in enumerate(article_urls, start=1):

        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()

            soup = BeautifulSoup(r.text, "html.parser")

            # Titre
            title_tag = soup.find(
                "h1",
                class_="mvp-post-title left entry-title"
            )
            title = title_tag.get_text(strip=True) if title_tag else None

            # Date
            time_tag = soup.find("time", class_="post-date updated")
            date_pub = time_tag.get("datetime") if time_tag else None

            # Contenu
            content_div = soup.find("div", id="mvp-content-main")

            content = ""
            if content_div:
                paragraphs = [
                    p.get_text(" ", strip=True)
                    for p in content_div.find_all("p")
                ]
                content = "\n\n".join(paragraphs)

            rows.append({
                "ID": idx,
                "Titre": title,
                "DatePublication": date_pub,
                "Contenu": content,
                "URL": url
            })

            sleep(sleep_time)

        except Exception as e:
            print(f"Erreur sur {url}: {e}")

    return pd.DataFrame(rows)