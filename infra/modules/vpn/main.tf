# TODO: rework to use custom ec2 module

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

resource "aws_key_pair" "openvpn" {
  key_name   = "${var.app_name}-openvpn"
  public_key = tls_private_key.this.public_key_openssh
}

resource "aws_instance" "openvpn" {
  ami                         = data.aws_ami.amazon_linux_2.id
  associate_public_ip_address = true
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.openvpn.key_name
  subnet_id                   = var.subnet_id

  vpc_security_group_ids = [
    aws_security_group.openvpn.id,
    aws_security_group.ssh_from_local.id,
  ]

  root_block_device {
    volume_type           = "gp2"
    volume_size           = var.instance_root_block_device_volume_size
    delete_on_termination = true
  }

  tags = local.all_tags
}

resource "null_resource" "openvpn_bootstrap" {
  connection {
    type        = "ssh"
    host        = aws_instance.openvpn.public_ip
    user        = var.ec2_username
    port        = "22"
    private_key = tls_private_key.this.private_key_pem
    agent       = false
  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "curl -O ${var.openvpn_install_script_location}",
      "chmod +x openvpn-install.sh",
      <<EOT
      sudo AUTO_INSTALL=y \
           APPROVE_IP=${aws_instance.openvpn.public_ip} \
           ENDPOINT=${aws_instance.openvpn.public_dns} \
           ./openvpn-install.sh

EOT
      ,
    ]
  }
}

resource "null_resource" "openvpn_update_users_script" {
  depends_on = [null_resource.openvpn_bootstrap]

  triggers = {
    ovpn_users = join(" ", var.ovpn_users)
  }

  connection {
    type        = "ssh"
    host        = aws_instance.openvpn.public_ip
    user        = var.ec2_username
    port        = "22"
    private_key = tls_private_key.this.private_key_pem
    agent       = false
  }

  provisioner "file" {
    source      = "${path.module}/scripts/update_users.sh"
    destination = "/home/${var.ec2_username}/update_users.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x ~${var.ec2_username}/update_users.sh",
      "sudo ~${var.ec2_username}/update_users.sh ${join(" ", var.ovpn_users)}",
    ]
  }
}

resource "null_resource" "openvpn_download_configurations" {
  depends_on = [null_resource.openvpn_update_users_script]

  triggers = {
    ovpn_users = join(" ", var.ovpn_users)
  }

  provisioner "local-exec" {
    command = <<EOT
    mkdir -p ${var.output_directory}/ovpn-config;
    scp -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -i ${local_file.private_key.filename} ${var.ec2_username}@${aws_instance.openvpn.public_ip}:/home/${var.ec2_username}/*.ovpn ${var.output_directory}/ovpn-config/

EOT

  }
}

resource "aws_security_group" "openvpn" {
  name        = "openvpn"
  description = "Allow inbound UDP access to OpenVPN and unrestricted egress"

  vpc_id = var.vpc_id

  tags = local.all_tags

  ingress {
    from_port   = 1194
    to_port     = 1194
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "http" "local_ip_address" {
  url = "http://ipv4.icanhazip.com"
}

locals {
  local_ip_address = "${chomp(data.http.local_ip_address.response_body)}/32"
  all_tags = merge(
    var.tags,
    {
      Name = "${var.app_name}-openvpn"
    },
  )
  secrets = {
    OPENVPN_CONFIG_CONTENTS = data.local_file.config_file.content
  }
}

resource "aws_security_group" "ssh_from_local" {
  name        = "ssh-from-local"
  description = "Allow SSH access only from local machine"

  vpc_id = var.vpc_id

  tags = local.all_tags

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.local_ip_address]
  }
}

data "local_file" "config_file" {
  # TODO: should not hard-code user.ovpn, will depend on the passed users and should have one file for each
  filename = "${var.output_directory}/ovpn-config/user.ovpn"
  depends_on = [
    null_resource.openvpn_download_configurations
  ]
}
