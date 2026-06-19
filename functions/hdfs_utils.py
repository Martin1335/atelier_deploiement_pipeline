import os
from typing import Optional

import pandas as pd
import requests


DEFAULT_HDFS_NAMENODE = os.getenv(
    "HDFS_NAMENODE_URL",
    "http://localhost:9870",
)
DEFAULT_HDFS_USER = os.getenv("HDFS_USER", "root")
DEFAULT_HDFS_BASE_PATH = os.getenv(
    "HDFS_BASE_PATH",
    "/user/root/legorafi_pipeline",
)


def _build_webhdfs_url(path: str, op: str, *, overwrite: bool = False) -> str:
    base = DEFAULT_HDFS_NAMENODE.rstrip("/")
    user = DEFAULT_HDFS_USER
    url = f"{base}/webhdfs/v1{path}?op={op}&user.name={user}"

    if overwrite:
        url += "&overwrite=true"

    return url


def _ensure_directory(path: str) -> None:
    response = requests.put(
        _build_webhdfs_url(path, "MKDIRS") + "&createParent=true",
        timeout=30,
    )
    response.raise_for_status()

    payload = response.json()
    if not payload.get("boolean", False):
        raise RuntimeError(
            f"Impossible de créer le répertoire HDFS : {path}"
        )


def write_dataframe_to_hdfs(
    df: pd.DataFrame,
    relative_path: str,
    *,
    hdfs_base_path: Optional[str] = None,
) -> str:
    """
    Envoie un DataFrame vers HDFS via l'API WebHDFS.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame à écrire.
    relative_path : str
        Chemin relatif à enregistrer sous la base HDFS (ex: raw/articles.csv).
    hdfs_base_path : str | None
        Base HDFS optionnelle. Si None, utilise la variable d'env.

    Returns
    -------
    str
        Chemin HDFS final utilisé.
    """
    base_path = hdfs_base_path or DEFAULT_HDFS_BASE_PATH
    target_path = f"{base_path.rstrip('/')}/{relative_path.lstrip('/')}"

    directory = os.path.dirname(target_path)
    _ensure_directory(directory)

    csv_content = df.to_csv(index=False, encoding="utf-8-sig")
    payload = csv_content.encode("utf-8")

    url = _build_webhdfs_url(target_path, "CREATE", overwrite=True)
    response = requests.put(
        url,
        data=payload,
        headers={"Content-Type": "application/octet-stream"},
        timeout=60,
        allow_redirects=True,
    )
    response.raise_for_status()

    return target_path
