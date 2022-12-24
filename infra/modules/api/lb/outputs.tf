output "target_group_arns" {
  description = "ARNs of the target groups. Useful for passing to your Auto Scaling group."
  value       = module.lb.target_group_arns
}

output "lb_dns_name" {
  description = "The DNS name of the load balancer"
  value       = module.lb.lb_dns_name
}
