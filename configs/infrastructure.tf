# infrastructure.tf
resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  port                 = 5432
  publicly_accessible  = true  # Security Risk!
}