output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC Id"
}

output "cluster_id" {
  value       = aws_ecs_cluster.main.id
  description = "ECS Cluster Id"
}

output "DNS_Name" {
  value       = aws_lb.frontend_alb.dns_name
  description = "DNS name for ALB frontend"
}