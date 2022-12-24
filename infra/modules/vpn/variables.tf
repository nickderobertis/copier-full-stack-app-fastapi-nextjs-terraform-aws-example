variable "vpc_id" {
  type        = string
  description = "ID of AWS VPC to put the VPN in"
}

variable "subnet_id" {
  type        = string
  description = "ID of AWS subnet to put the VPN in. Should be in the same VPC matching the passed vpc_id"
}

variable "tags" {
  type        = map(string)
  description = "Tags to apply to the VPN"
}

variable "cidr_block" {
  description = "The CIDR block range to use for the OpenVPN VPC"
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "The instance type to use"
  default     = "t2.micro"
}

variable "instance_root_block_device_volume_size" {
  description = "The size of the root block device volume of the EC2 instance in GiB"
  default     = 8
}

variable "ec2_username" {
  description = "The user to connect to the EC2 as"
  default     = "ec2-user"
}

variable "openvpn_install_script_location" {
  description = "The location of an OpenVPN installation script compatible with https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh"
  default     = "https://raw.githubusercontent.com/dumrauf/openvpn-install/master/openvpn-install.sh"
}

variable "ovpn_users" {
  type        = list(string)
  description = "The list of users to automatically provision with OpenVPN access"
  default     = ["user"]
}

variable "output_directory" {
  description = "The name of the directory to download the OVPN configuration files and keys to"
  default     = "generated"
}

variable "app_name" {
  type        = string
  description = "The name of the application"
}
