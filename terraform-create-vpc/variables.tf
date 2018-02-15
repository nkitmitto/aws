variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "aws_region" {
    description = "EC2 Region for the VPC"
    default = "us-west-2"
}

variable "vpc_name" {
    description = "Name of the VPC"
    default = "prod-vpc"
}

variable "vpc_cidr" {
    description = "CIDR for the whole VPC"
    default = "10.0.0.0/16"
}

variable "public-a_subnet_cidr" {
    description = "CIDR for the Public Subnet"
    default = "10.0.4.0/24"
}

variable "public-b_subnet_cidr" {
    description = "CIDR for the Public Subnet"
    default = "10.0.5.0/24"
}

variable "public-c_subnet_cidr" {
    description = "CIDR for the Public Subnet"
    default = "10.0.6.0/24"
}

variable "private-a_subnet_cidr" {
    description = "CIDR for the Private Subnet"
    default = "10.0.1.0/24"
}

variable "private-b_subnet_cidr" {
    description = "CIDR for the Private Subnet"
    default = "10.0.2.0/24"
}

variable "private-c_subnet_cidr" {
    description = "CIDR for the Private Subnet"
    default = "10.0.3.0/24"
}
