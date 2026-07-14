data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "news_analyzer" {
  function_name    = "news-analyzer-fixed-response"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  role             = data.aws_iam_role.lab_role.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.news_analyzer.function_name
}