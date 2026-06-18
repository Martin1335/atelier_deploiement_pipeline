import pandas as pd
import re


def clean_legorafi_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et valide un DataFrame issu du scraper Le Gorafi.

    Étapes :
    - suppression des doublons
    - nettoyage des textes
    - suppression des lignes invalides
    - normalisation des dates (si possible)
    """

    df = df.copy()

    # ==========================
    # 1. Suppression doublons
    # ==========================
    df = df.drop_duplicates(subset=["URL"])

    # ==========================
    # 2. Nettoyage texte
    # ==========================
    def clean_text(text):
        if not isinstance(text, str):
            return None

        text = text.replace("\xa0", " ")  # espaces insécables
        text = re.sub(r"\s+", " ", text)  # espaces multiples
        text = text.strip()

        return text if text else None

    df["Titre"] = df["Titre"].apply(clean_text)
    df["Contenu"] = df["Contenu"].apply(clean_text)

    # ==========================
    # 3. Vérification qualité minimale
    # ==========================
    df = df[
        df["Titre"].notnull() &
        df["Contenu"].notnull() &
        (df["Contenu"].str.len() > 50)  # évite contenus trop vides
    ]

    # ==========================
    # 4. Normalisation dates
    # ==========================
    df["DatePublication"] = pd.to_datetime(
        df["DatePublication"],
        errors="coerce"
    )

    # ==========================
    # 5. Réindexation propre
    # ==========================
    df = df.reset_index(drop=True)
    df.insert(0, "ID", range(1, len(df) + 1))

    return df