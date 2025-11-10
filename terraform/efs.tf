# EFS cho volume backend books-service
# NOTE: Nên dùng EFS Access Point nếu có nhiều container cùng truy cập
resource "aws_efs_file_system" "backend_b_fs" {
  creation_token = "${var.project_name}-efs"
  encrypted      = true

  tags = {
    Name = "${var.project_name}-backend2-efs"
  }
}

resource "aws_efs_mount_target" "backend_b_fs_mt" {
  count           = length(aws_subnet.private)
  file_system_id  = aws_efs_file_system.backend_b_fs.id
  subnet_id       = aws_subnet.private[count.index].id
  security_groups = [aws_security_group.efs.id]
}