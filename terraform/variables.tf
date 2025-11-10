variable "aws_region" {
  type    = string
  default = "ap-southeast-1"
}

variable "project_name" {
  description = "Project name, prefix for AWS resources"
  type        = string
  default     = "book-mg"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "Public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnets" {
  description = "Private subnets"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "backend_a_image" {
  description = "Docker image for backend auth service"
  type        = string
  default     = "peterhoward/books-auth-api"
}

variable "backend_b_image" {
  description = "Docker image for backend book service"
  type        = string
  default     = "peterhoward/books-book-api"
}

variable "frontend_image" {
  description = "Docker image for frontend service"
  type        = string
  default     = "peterhoward/books-frontend"
}

# Database secret
variable "mongodb_host" {
  type      = string
  sensitive = true
}

variable "mongodb_username" {
  type      = string
  sensitive = true
}

variable "mongodb_password" {
  type      = string
  sensitive = true
}

variable "jwt_secret_key" {
  type      = string
  sensitive = true
}