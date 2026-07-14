data "aws_iam_role" "lab_role" {
  name = "LabRole"
}

output "lab_role_arn" {
  value = data.aws_iam_role.lab_role.arn
}