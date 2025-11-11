# NOTE: Chỉ dùng 1 trong 2 nguồn (cidr_ipv4 hoặc referenced_security_group_id) khi chỉ định rule
# Security group backend
resource "aws_security_group" "backend" {
  name   = "${var.project_name}-backend-sg"
  vpc_id = aws_vpc.main.id
}

resource "aws_vpc_security_group_ingress_rule" "allow_all_vpc_traffic" {
  security_group_id = aws_security_group.backend.id
  cidr_ipv4         = aws_vpc.main.cidr_block # Cho phép traffic trong VPC truy cập (private)
  from_port         = 5000
  to_port           = 5001
  ip_protocol       = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4_to_backend" {
  security_group_id = aws_security_group.backend.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# Secuity group frontend
resource "aws_security_group" "frontend" {
  name   = "${var.project_name}-frontend-sg"
  vpc_id = aws_vpc.main.id
}

# Chỉ nhận traffic từ ALB thay vì VPC
resource "aws_vpc_security_group_ingress_rule" "allow_traffic_from_alb" {
  security_group_id            = aws_security_group.frontend.id
  referenced_security_group_id = aws_security_group.alb.id # Cho phép frontend inbound từ ALB
  from_port                    = 80
  to_port                      = 80
  ip_protocol                  = "tcp"
  description                  = "Only allow traffic from ALB of frontend"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4_to_frontend" {
  security_group_id = aws_security_group.frontend.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# Security group EFS
resource "aws_security_group" "efs" {
  name        = "${var.project_name}-efs-sg"
  vpc_id      = aws_vpc.main.id
  description = "Allow NFS traffic from backend"
}

resource "aws_vpc_security_group_ingress_rule" "efs_in" {
  security_group_id            = aws_security_group.efs.id
  referenced_security_group_id = aws_security_group.backend.id
  from_port                    = 2049
  to_port                      = 2049
  ip_protocol                  = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "efs_out" {
  security_group_id = aws_security_group.efs.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# Security group ALB cho frontend
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  vpc_id      = aws_vpc.main.id
  description = "Security group for ALB frontend"
}

resource "aws_vpc_security_group_ingress_rule" "alb_allow_http_in" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0" # Cho phép mọi traffic Internet truy cập (public)
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
  description       = "Allow HTTP traffic from anywhere"
}

resource "aws_vpc_security_group_egress_rule" "alb_allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.alb.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
  description       = "Allow ALB to reach all outbound traffic"
}