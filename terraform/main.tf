terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "futureyou-cluster"
}

# ECR Repository
resource "aws_ecr_repository" "backend" {
  name = "futureyou-backend"
  image_scanning_configuration {
    scan_on_push = true
  }
}

# S3 for Frontend
resource "aws_s3_bucket" "frontend" {
  bucket = "futureyou-frontend"
}

# CloudFront
resource "aws_cloudfront_distribution" "frontend" {
  enabled = true
  default_root_object = "index.html"
  
  origin {
    domain_name = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id   = "S3-frontend"
  }
  
  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-frontend"
    viewer_protocol_policy = "redirect-to-https"
    
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

output "cloudfront_domain" {
  value = aws_cloudfront_distribution.frontend.domain_name
}
