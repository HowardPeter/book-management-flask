# ECS cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
}

# Task definition (3 service)
resource "aws_ecs_task_definition" "backend_a" {
  family                   = "books-auth-task"
  network_mode             = "awsvpc" # Hỗ trợ service discovery
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 3072

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([{
    name      = "books-auth-container"
    image     = "${var.backend_a_image}"
    essential = true
    portMappings = [{
      containerPort = 5000
      protocol      = "tcp"
    }]
    environment = [
      { name = "APP_ENV", value = "production" },
      { name = "MONGODB_HOST", value = "${var.mongodb_host}" },
      { name = "MONGODB_DB", value = "users" },
      { name = "JWT_SECRET_KEY", value = "${var.jwt_secret_key}" },
      { name = "MONGODB_PASSWORD", value = "${var.mongodb_password}" },
      { name = "MONGODB_USERNAME", value = "${var.mongodb_username}" }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/books-auth-task"
        "awslogs-region"        = "ap-southeast-1"
        "awslogs-stream-prefix" = "ecs"
        "awslogs-create-group"  = "true"
      }
    }
  }])
}

resource "aws_ecs_task_definition" "backend_b" {
  family                   = "books-book-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 3072

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role_backend.arn

  volume {
    name = "book-uploads"
    efs_volume_configuration {
      file_system_id     = aws_efs_file_system.backend_b_fs.id
      transit_encryption = "ENABLED"
    }
  }

  container_definitions = jsonencode([{
    name      = "books-book-container"
    image     = "${var.backend_b_image}"
    essential = true
    portMappings = [{
      containerPort = 5001
      protocol      = "tcp"
    }]
    environment = [
      { name = "APP_ENV", value = "production" },
      { name = "MONGODB_HOST", value = "${var.mongodb_host}" },
      { name = "MONGODB_DB", value = "books" },
      { name = "JWT_SECRET_KEY", value = "${var.jwt_secret_key}" },
      { name = "MONGODB_PASSWORD", value = "${var.mongodb_password}" },
      { name = "MONGODB_USERNAME", value = "${var.mongodb_username}" }
    ]
    mountPoints = [{
      sourceVolume  = "book-uploads"
      containerPath = "/app/uploads"
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/books-book-task"
        "awslogs-region"        = "ap-southeast-1"
        "awslogs-stream-prefix" = "ecs"
        "awslogs-create-group"  = "true"
      }
    }
  }])
}

resource "aws_ecs_task_definition" "frontend" {
  family                   = "books-frontend-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 3072

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([{
    name      = "books-frontend-container"
    image     = "${var.frontend_image}"
    essential = true
    portMappings = [{
      containerPort = 80
      protocol      = "tcp"
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/"
        "awslogs-region"        = "ap-southeast-1"
        "awslogs-stream-prefix" = "ecs"
        "awslogs-create-group"  = "true"
      }
    }
  }])
}

# ECS Services
resource "aws_ecs_service" "backend_a" {
  name            = "books-auth-task-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend_a.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = aws_subnet.private[*].id
    security_groups = [aws_security_group.backend.id]
  }

  service_registries {
    registry_arn = aws_service_discovery_service.auth.arn
  }
}

resource "aws_ecs_service" "backend_b" {
  name            = "books-book-task-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend_b.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = aws_subnet.private[*].id
    security_groups = [aws_security_group.backend.id]
  }

  service_registries {
    registry_arn = aws_service_discovery_service.book.arn
  }
}

resource "aws_ecs_service" "frontend" {
  name            = "books-react-task-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.frontend.id]
    assign_public_ip = true # Gán Public IP để IGW hoạt động, service backend đã có NAT Gateway
  }

  service_registries {
    registry_arn = aws_service_discovery_service.frontend.arn
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.frontend_tg.arn
    container_name   = "books-frontend-container" # Frontend task definition container
    container_port   = 80
  }
}