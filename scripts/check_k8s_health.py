# scripts/check_k8s_health.py
import json

def get_status():
    status = {
        "cluster": "prod-useast-01",
        "nodes": 5,
        "unhealthy_pods": ["auth-service-v2", "payment-gateway-6f8"],
        "error": "ImagePullBackOff in namespace 'billing'"
    }
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    get_status()