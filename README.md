# 📰 News Analyzer

**Cloud Computing Capstone · Group 6**  
**Keshav Virajbhai Kansara (100007269) & Joemon Johnson (100006681)**  

---

## What It Does

News Analyzer is a fully serverless cloud application that fetches live
news headlines from NewsAPI, stores them in DynamoDB, and displays them
on a web interface. Every request triggers an AWS Lambda function that
reads the API key securely from Secrets Manager, calls NewsAPI, saves
the results to DynamoDB, and returns the articles to the caller.

The entire infrastructure is provisioned with Terraform — no manual
clicking in the AWS console.

---

## Architecture

User / Browser
↓
API Gateway (HTTP API — public HTTPS endpoint)
↓
AWS Lambda (Python 3.12 — runs under LabRole)
↓ ↓
Secrets Manager NewsAPI (external)
(reads API key) (fetches headlines)
↓
DynamoDB
(stores articles)
↓
CloudWatch
(logs & monitoring)

---

## Services Used

| Service | Role |
|---|---|
| AWS Lambda | Serverless compute (Python 3.12) |
| API Gateway (HTTP API) | Public HTTPS endpoint |
| Secrets Manager | Secure API key storage |
| DynamoDB (PAY_PER_REQUEST) | Zero idle cost database |
| CloudWatch | Logs and monitoring |
| NewsAPI | External news data source |
| Terraform | Infrastructure as Code |

---

## Project Structure

├── main.tf # AWS provider + region config
├── iam.tf # LabRole data source (no role creation)
├── lambda.tf # Lambda function + zip packaging
├── apigateway.tf # API Gateway + routes + CORS config
├── secrets.tf # Secrets Manager secret container
├── dynamodb.tf # DynamoDB table (PAY_PER_REQUEST)
├── lambda/
│ └── handler.py # Lambda handler — fetches + stores news
├── index.html # Frontend webpage
├── .gitignore # Excludes secrets, state, and zip files
└── README.md # This file

---

## How To Deploy

### Prerequisites
- AWS CLI installed and configured with valid credentials
- Terraform installed
- Python 3.x installed
- NewsAPI key from [newsapi.org](https://newsapi.org)

### Step 1 — Clone the repo
```bash
git clone https://github.com/manches3003/News_summariser
cd News_summariser
```

### Step 2 — Initialize Terraform
```bash
terraform init
```

### Step 3 — Deploy infrastructure
```bash
terraform apply
```
Type `yes` when prompted. This creates Lambda, API Gateway,
Secrets Manager, and DynamoDB.

### Step 4 — Set your NewsAPI key
```bash
aws secretsmanager put-secret-value \
  --secret-id news-api-key \
  --secret-string "{\"api_key\":\"YOUR_NEWSAPI_KEY_HERE\"}" \
  --region us-east-1
```
On Windows PowerShell:
```powershell
aws secretsmanager put-secret-value --secret-id news-api-key --secret-string '{\"api_key\":\"YOUR_NEWSAPI_KEY_HERE\"}' --region us-east-1
```

### Step 5 — Start the frontend
```bash
python -m http.server 8080
```
Open `http://localhost:8080/index.html` in your browser and click
**Fetch Latest News**.

---

## API Endpoint

GET https://yzmafcftkd.execute-api.us-east-1.amazonaws.com//news

Returns a JSON response with the top 10 US headlines:
```json
{
  "articles": [
    {
      "title": "Article headline here",
      "source": "BBC News",
      "description": "Short description...",
      "url": "https://...",
      "publishedAt": "2026-07-20T13:37:07Z"
    }
  ]
}
```

---

## Important Notes

- **Do NOT commit AWS credentials or API keys** — the `.gitignore`
  excludes all sensitive files
- The Lambda runs under the existing **LabRole** — no IAM role is
  created (Learner Lab blocks `iam:CreateRole`)
- DynamoDB uses **PAY_PER_REQUEST** billing — zero cost at idle
- AWS Learner Lab credentials expire every session — refresh them
  from AWS Details before running `terraform apply`
- Run `terraform destroy` after the demo to avoid unexpected charges

---

## Tear Down

```bash
terraform destroy
```
Type `yes` when prompted. This removes all AWS resources.

