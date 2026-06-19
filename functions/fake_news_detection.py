import requests
import pandas as pd


def enrich_with_fake_news_detection(
    df: pd.DataFrame,
    api_url: str = "http://localhost:5001/detect_json",
    timeout: int = 30,
) -> pd.DataFrame:
    """
    Enrichit un DataFrame avec une colonne 'is_fake_news'
    en interrogeant une API de détection de fake news.

    Paramètres
    ----------
    df : pd.DataFrame
        Doit contenir les colonnes 'Titre' et 'Contenu'.

    api_url : str
        URL de l'API de détection.

    timeout : int
        Timeout HTTP en secondes.

    Returns
    -------
    pd.DataFrame
        DataFrame enrichi avec la colonne 'is_fake_news'.
    """

    df = df.copy()

    results = []

    for _, row in df.iterrows():

        title = row.get("Titre", "") or ""
        content = row.get("Contenu", "") or ""

        text = f"{title}\n\n{content}"

        try:
            response = requests.post(
                api_url,
                json={"text": text},
                timeout=timeout,
            )

            response.raise_for_status()

            result = response.json()

            # Cas 1 :
            # {"result": "Fake"}
            if "result" in result:
                results.append(result["result"])

            # Cas inconnu
            else:
                results.append(result)

        except Exception as e:
            print(
                f"Erreur détection article ID={row.get('ID')} : {e}"
            )
            results.append(None)

    df["is_fake_news"] = results

    return df