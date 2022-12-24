data "aws_ami" "amazon_linux_2" {
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "block-device-mapping.volume-type"
    values = ["gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["amazon"]
}

resource "tls_private_key" "this" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key" {
  content         = tls_private_key.this.private_key_pem
  filename        = "${var.output_directory}/key"
  file_permission = "0600"
}

resource "local_file" "public_key" {
  content         = tls_private_key.this.public_key_openssh
  filename        = "${var.output_directory}/key.pub"
  file_permission = "0644"
}

resource "aws_key_pair" "this" {
  key_name   = var.instance_name
  public_key = tls_private_key.this.public_key_openssh
}

resource "aws_instance" "this" {
  ami                         = data.aws_ami.amazon_linux_2.id
  associate_public_ip_address = true
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.this.key_name
  subnet_id                   = var.subnet_id
  iam_instance_profile = var.iam_instance_profile

  vpc_security_group_ids = concat([
    aws_security_group.ssh_from_local.id,
  ], var.security_group_ids)

  root_block_device {
    volume_type           = "gp2"
    volume_size           = var.instance_root_block_device_volume_size
    delete_on_termination = true
  }

  user_data = <<-EOF
Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
${var.startup_script}
--//--
  EOF

  tags = merge(var.tags, {Name = var.instance_name})
}

data "http" "local_ip_address" {
  url = "http://ipv4.icanhazip.com"
}

locals {
  local_ip_address = "${chomp(data.http.local_ip_address.response_body)}/32"
}

resource "aws_security_group" "ssh_from_local" {
  name        = "${var.instance_name}-ssh-from-local"
  description = "Allow SSH access only from local machine"

  vpc_id = var.vpc_id

  tags = var.tags

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.local_ip_address]
  }
}
