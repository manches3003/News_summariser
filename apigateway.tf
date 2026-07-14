resource "aws_apigatewayv2_api" "news_api" {
  name          = "news-analyzer-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.news_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.news_analyzer.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.news_api.id
  route_key = "GET /news"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.news_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "apigw_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.news_analyzer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.news_api.execution_arn}/*/*"
}

output "api_endpoint" {
  value = "${aws_apigatewayv2_stage.default_stage.invoke_url}/news"
}