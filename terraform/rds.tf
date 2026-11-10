# Security Group autorisant l'accès à PostgreSQL (port 5432)
resource "aws_security_group" "rds_sg" {
  name        = "${var.project_name}-rds-sg"
  description = "Autoriser le trafic PostgreSQL entrant pour dbt et le pipeline"

  ingress {
    description = "PostgreSQL depuis votre IP ou conteneur local"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    # Pour un test dev, vous pouvez restreindre a votre IP publique (ex: "votre.ip/32")
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-rds-sg"
    Environment = var.environment
  }
}

# Instance AWS RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier             = "${var.project_name}-db"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = "db.t3.micro"
  db_name                = "f1_db"
  username               = "f1_admin"
  password               = "ChangeMeStrongPassword123!" # A remplacer ou passer par variable sensible
  publicly_accessible    = true
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  tags = {
    Name        = "${var.project_name}-rds"
    Environment = var.environment
  }
}