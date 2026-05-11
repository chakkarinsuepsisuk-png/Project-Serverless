
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "projectcloud-496006"
  region  = "asia-southeast1"
}

resource "google_sql_database_instance" "main" {
  name             = "it-repair-db-fast"
  database_version = "MYSQL_8_0"
  region           = "asia-southeast1"

  settings {
    tier = "db-f1-micro" # สเปคเล็กสุด ประหยัดเงิน
    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "all-access"
        value = "0.0.0.0/0" # เปิดให้รันเทสได้จากทุกที่
      }
    }
  }
  deletion_protection = false
}

resource "google_sql_database" "database" {
  name     = "it_repair"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "users" {
  name     = "root"
  instance = google_sql_database_instance.main.name
  password = "SuperSecretPassword123!"
}

output "db_public_ip" {
  value = google_sql_database_instance.main.public_ip_address
}