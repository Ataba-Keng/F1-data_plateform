terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  layers = toset(["raw", "staging", "marts"])
}

# Création des 3 compartiments S3 Medallion
resource "aws_s3_bucket" "datalake_layers" {
  for_each      = local.layers
  bucket        = "${var.project_name}-${each.key}-${var.environment}"
  force_destroy = true

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Layer       = each.key
  }
}

# Chiffrement par défaut (SSE-S3)
resource "aws_s3_bucket_server_side_encryption_configuration" "sse" {
  for_each = aws_s3_bucket.datalake_layers

  bucket = each.value.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Blocage de tout accès public
resource "aws_s3_bucket_public_access_block" "public_block" {
  for_each = aws_s3_bucket.datalake_layers

  bucket = each.value.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}