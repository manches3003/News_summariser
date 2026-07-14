import json
import boto3
import urllib.request
import uuid
from datetime import datetime

def lambda_handler(event, context):
    # Step 1: Get API key from Secrets Manager
    secrets_client = boto3.client("secretsmanager", region_name="us-east-1")
    secret = secrets_client.get_secret_value(SecretId="news-api-key")
    api_key = json.loads(secret["SecretString"])["api_key"]

    # Step 2: Call NewsAPI
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode())

    # Step 3: Get top 5 articles
    articles = [
        {"title": a["title"], "source": a["source"]["name"]}
        for a in data.get("articles", [])[:5]
    ]

    # Step 4: Save to DynamoDB
    dynamo = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamo.Table("news-analyzer-articles")
    
    for article in articles:
        table.put_item(Item={
            "article_id": str(uuid.uuid4()),
            "title": article["title"],
            "source": article["source"],
            "fetched_at": datetime.utcnow().isoformat()
        })

    # Step 5: Return articles
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"articles": articles})
    }