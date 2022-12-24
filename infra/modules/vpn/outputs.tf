output "ec2_instance_ip" {
  value = aws_instance.openvpn.public_ip
}

output "private_key_file" {
  value = local_file.private_key.filename
}

output "public_key_file" {
  value = local_file.public_key.filename
}

output "connection_string" {
  value = "'ssh -i ${local_file.private_key.filename} ${var.ec2_username}@${aws_instance.openvpn.public_ip}'"
}

output "ovpn_config_contents" {
  value     = data.local_file.config_file.content
  sensitive = true
}

output "secrets" {
  value     = local.secrets
  sensitive = true
}
