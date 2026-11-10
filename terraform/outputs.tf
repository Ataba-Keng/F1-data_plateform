output "raw_bucket_name" {
  value       = aws_s3_bucket.datalake_layers["raw"].bucket
  description = "Nom du compartiment S3 pour la couche Raw"
}

output "staging_bucket_name" {
  value       = aws_s3_bucket.datalake_layers["staging"].bucket
  description = "Nom du compartiment S3 pour la couche Staging"
}

output "marts_bucket_name" {
  value       = aws_s3_bucket.datalake_layers["marts"].bucket
  description = "Nom du compartiment S3 pour la couche Marts"
}

output "rds_endpoint" {
  value       = aws_db_instance.postgres.address
  description = "Hote de connexion RDS PostgreSQL"
}