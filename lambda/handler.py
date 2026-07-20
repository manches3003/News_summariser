import json
import boto3
import urllib.request
import uuid
from datetime import datetime

def lambda_handler(event, context):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    secret = client.get_secret_value(SecretId="news-api-key")
    api_key = json.loads(secret["SecretString"])["api_key"]

    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=10&apiKey={api_key}"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode())

    articles = []
    for a in data.get("articles", []):
        articles.append({
            "title": a.get("title", ""),
            "source": a["source"]["name"],
            "description": a.get("description", "No summary available."),
            "url": a.get("url", ""),
            "publishedAt": a.get("publishedAt", "")
        })

    dynamo = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamo.Table("news-analyzer-articles")
    for article in articles:
        table.put_item(Item={
            "article_id": str(uuid.uuid4()),
            "title": article["title"],
            "source": article["source"],
            "fetched_at": datetime.utcnow().isoformat()
        })

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"articles": articles})
    }