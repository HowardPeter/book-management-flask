# Service discovery namespace cho ECS service
resource "aws_service_discovery_private_dns_namespace" "service_discovery" {
  name        = "book-management.local"
  description = "Service discovery namespace for book management services"
  vpc         = aws_vpc.main.id
}

# Service discovery service
resource "aws_service_discovery_service" "auth" {
  name        = "auth"
  description = "Service discovery for auth service"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.service_discovery.id

    dns_records {
      ttl  = 15
      type = "A"
    }
  }
}

resource "aws_service_discovery_service" "book" {
  name        = "book"
  description = "Service discovery for book service"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.service_discovery.id

    dns_records {
      ttl  = 15
      type = "A"
    }
  }
}

resource "aws_service_discovery_service" "frontend" {
  name        = "frontend"
  description = "Service discovery for frontend service"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.service_discovery.id

    dns_records {
      ttl  = 15
      type = "A"
    }
  }
}