resource "aws_dynamodb_table" "news_analyzer" {
  name         = "news-analyzer-articles"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "article_id"

  attribute {
    name = "article_id"
    type = "S"
  }
}