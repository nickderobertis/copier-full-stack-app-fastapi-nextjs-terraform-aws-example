output "instance_ip" {
  value = aws_instance.this.public_ip
}

output "public_dns" {
  value = aws_instance.this.public_dns
}

output "instance_id" {
  value = aws_instance.this.id
}

output "private_key_file" {
  value = local_file.private_key.filename
}

output "public_key_file" {
  value = local_file.public_key.filename
}

output "connection_string" {
  value = "ssh -i ${local_file.private_key.filename} ec2-user@${aws_instance.this.public_ip}"
}
