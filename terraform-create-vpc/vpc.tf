/*
    Require Terraform 0.8.8
*/
terraform {
    required_version = "> 0.8.8"
}

/*
    Create VPC and Internet Gateway
*/
resource "aws_vpc" "default" {
    cidr_block = "${var.vpc_cidr}"
    enable_dns_hostnames = true
    tags {
        Name = "${var.vpc_name}"
    }
}

resource "aws_internet_gateway" "default" {
    vpc_id = "${aws_vpc.default.id}"
}

/*
  Public A Subnet
*/
resource "aws_subnet" "a-public" {
    vpc_id = "${aws_vpc.default.id}"

    cidr_block = "${var.public-a_subnet_cidr}"
    availability_zone = "us-west-2a"

    tags {
        Name = "Public Subnet - A"
    }
}
/*
    Create Route Table for Public subnets
*/
resource "aws_route_table" "public-rt" {
    vpc_id = "${aws_vpc.default.id}"

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.default.id}"
    }

    tags {
        Name = "Public Subnet Route Table"
    }
}

/*
  Public B Subnet
*/
resource "aws_subnet" "b-public" {
    vpc_id = "${aws_vpc.default.id}"

    cidr_block = "${var.public-b_subnet_cidr}"
    availability_zone = "us-west-2b"

    tags {
        Name = "Public Subnet - B"
    }
}

/*
  Public C Subnet
*/
resource "aws_subnet" "c-public" {
    vpc_id = "${aws_vpc.default.id}"

    cidr_block = "${var.public-c_subnet_cidr}"
    availability_zone = "us-west-2c"

    tags {
        Name = "Public Subnet - C"
    }
}

/*
  Subnet and Route Table Associations for Public Subnets
*/
resource "aws_route_table_association" "a-public" {
    subnet_id = "${aws_subnet.a-public.id}"
    route_table_id = "${aws_route_table.public-rt.id}"
}
resource "aws_route_table_association" "b-public" {
    subnet_id = "${aws_subnet.b-public.id}"
    route_table_id = "${aws_route_table.public-rt.id}"
}
resource "aws_route_table_association" "c-public" {
    subnet_id = "${aws_subnet.c-public.id}"
    route_table_id = "${aws_route_table.public-rt.id}"
}

/*
  Private A Subnet
*/
resource "aws_subnet" "a-private" {
    vpc_id = "${aws_vpc.default.id}"

    cidr_block = "${var.private-a_subnet_cidr}"
    availability_zone = "us-west-2a"

    tags {
        Name = "Private Subnet - A"
    }
}

/*
    Create route table for Private subnets
*/
resource "aws_route_table" "private-rt" {
    vpc_id = "${aws_vpc.default.id}"

    route {
        cidr_block = "0.0.0.0/0"
        nat_gateway_id = "${aws_nat_gateway.gw.id}"
    }

    tags {
        Name = "Private Subnet Route Table"
    }
}

/*
  Private B Subnet
*/
resource "aws_subnet" "b-private" {
    vpc_id = "${aws_vpc.default.id}"

    cidr_block = "${var.private-b_subnet_cidr}"
    availability_zone = "us-west-2b"

    tags {
        Name = "Private Subnet - B"
    }
}

/*
  Private C Subnet
*/
resource "aws_subnet" "c-private" {
    vpc_id = "${aws_vpc.default.id}"

    cidr_block = "${var.private-c_subnet_cidr}"
    availability_zone = "us-west-2c"

    tags {
        Name = "Private Subnet - C"
    }
}

/*
  Subnet and Route Table Associations for Private Subnets
*/
resource "aws_route_table_association" "a-private" {
    subnet_id = "${aws_subnet.a-private.id}"
    route_table_id = "${aws_route_table.private-rt.id}"
}

resource "aws_route_table_association" "b-private" {
    subnet_id = "${aws_subnet.b-private.id}"
    route_table_id = "${aws_route_table.private-rt.id}"
}
resource "aws_route_table_association" "c-private" {
    subnet_id = "${aws_subnet.c-private.id}"
    route_table_id = "${aws_route_table.private-rt.id}"
}

/*
  NAT Gateway
*/
resource "aws_nat_gateway" "gw" {
    allocation_id = "${aws_eip.nat.id}"
    subnet_id = "${aws_subnet.a-public.id}"
}

resource "aws_eip" "nat" {
    vpc = true
}
