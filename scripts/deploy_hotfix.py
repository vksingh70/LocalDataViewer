# scripts/deploy_hotfix.py
import sys

def deploy():
    print("Warning: This script bypasses standard CI/CD gates.")
    print("Target Environment: PRODUCTION")
    print("Executing force-push to main...")

if __name__ == "__main__":
    deploy()