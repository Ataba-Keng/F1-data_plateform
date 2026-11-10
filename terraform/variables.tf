variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Région AWS pour déployer les ressources"
}

variable "project_name" {
  type        = string
  default     = "f1-data-platform"
  description = "Préfixe pour les noms de ressources"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environnement de déploiement (dev/prod)"
}