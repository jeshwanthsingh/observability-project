terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "~> 0.0.15"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "observability" {
  name            = "observability"
  kubeconfig_path = "${path.root}/observability-config"
}
