# ALB để truy cập vào frontend
resource "aws_lb" "frontend_alb" {
  name               = "${var.project_name}-frontend-alb"
  load_balancer_type = "application"
  subnets            = aws_subnet.public[*].id
  security_groups    = [aws_security_group.alb.id]
}

resource "aws_lb_target_group" "frontend_tg" {
  name        = "${var.project_name}-frontend-lb-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    path                = "/index.html"
    protocol            = "HTTP"
    matcher             = "200-399"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3 # số lần thành công liên tiếp để coi là "healthy"
    unhealthy_threshold = 3 # số lần thất bại liên tiếp để coi là "unhealthy"
  }
}

resource "aws_lb_listener" "frontend_listener" {
  load_balancer_arn = aws_lb.frontend_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend_tg.arn
  }
}