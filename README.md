# Atelier Déploiement de Pipeline

Ceci est ma copie pour le module "Atelier Déploiement de Pipeline (Hadoop)".


## Analyse des besoins utilisateurs

On peut différencier deux groupes d'utilisateurs distincts :
- Les data scientists
- Les équipes BI

Les deux groupes d'utilisateurs ont besoin de données historiques complètes et nettoyées, même s'il est intéressant de pouvoir donner aux Data Scientists l'accès aux données non-nettoyés, dans le cadre de l'entraînement de leurs modèles.

## Stockage HDFS

Le pipeline envoie désormais les données dans trois emplacements HDFS :
- `raw/articles_raw.csv` : données brutes récupérées par le scraper
- `clean/articles_clean.csv` : données nettoyées après suppression des doublons et normalisation
- `processed/articles_processed.csv` : dataset final enrichi avec la colonne `is_fake_news`

## Pré-requis côté Hadoop

Pour que le projet fonctionne correctement, il faut :
1. lancer un cluster Hadoop (NameNode + DataNode)
2. démarrer l'API WebHDFS sur le NameNode
3. vérifier que l'URL de l'API est accessible (par défaut : `http://localhost:9870`)
4. assurer que l'utilisateur utilisé par Python a les droits d'écriture dans le dossier HDFS cible

## Commandes utiles

### Démarrer Hadoop localement

Si tu utilises un conteneur Docker pour Hadoop, utilise une image maintenue et compatible avec ton runtime Docker :
```bash
docker run -d \
  --name hadoop \
  -p 9870:9870 \
  -p 8088:8088 \
  apache/hadoop:3.5.0
```

### Vérifier l'accès à WebHDFS

```bash
curl "http://localhost:9870/webhdfs/v1/?op=GETHOMEDIRECTORY"
```

### Vérifier les répertoires HDFS

```bash
hdfs dfs -ls /
```

### Lancer le pipeline
```bash
python main.py
```

## Variables d'environnement

Le projet utilise les variables suivantes :
- `HDFS_NAMENODE_URL` : URL du NameNode (défaut : `http://localhost:9870`)
- `HDFS_USER` : utilisateur HDFS (défaut : `root`)
- `HDFS_BASE_PATH` : base du dossier de stockage (défaut : `/user/root/legorafi_pipeline`)

