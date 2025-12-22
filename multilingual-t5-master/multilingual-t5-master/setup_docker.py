#!/usr/bin/env python
"""
Setup script for Multilingual T5 project
Helps configure the environment and run the project
"""

import subprocess
import sys
import os
import platform

def check_docker():
    """Check if Docker is installed"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        print(f"✓ Docker found: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("✗ Docker not found. Please install Docker Desktop.")
        return False

def check_docker_compose():
    """Check if Docker Compose is installed"""
    try:
        result = subprocess.run(["docker-compose", "--version"], capture_output=True, text=True)
        print(f"✓ Docker Compose found: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("✗ Docker Compose not found.")
        return False

def build_docker_image():
    """Build Docker image"""
    print("\nBuilding Docker image...")
    result = subprocess.run(["docker", "build", "-t", "multilingual-t5:latest", "."])
    return result.returncode == 0

def run_docker_container():
    """Run Docker container"""
    print("\nStarting Docker container...")
    if platform.system() == "Windows":
        cmd = ["docker-compose", "up", "-d"]
    else:
        cmd = ["docker-compose", "up", "-d"]
    
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    print("=" * 60)
    print("Multilingual T5 - Environment Setup")
    print("=" * 60)
    
    # Check Docker
    if not check_docker():
        print("\nPlease install Docker Desktop from: https://www.docker.com/products/docker-desktop")
        sys.exit(1)
    
    if not check_docker_compose():
        print("\nInstalling Docker Compose...")
        # Docker Desktop includes Docker Compose on Windows
        print("Docker Compose should be included with Docker Desktop")
    
    print("\n" + "=" * 60)
    print("Setup Options:")
    print("=" * 60)
    print("1. Build Docker image")
    print("2. Run Docker container with Jupyter Lab")
    print("3. Run Docker container with bash shell")
    print("4. View Docker setup guide")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        if build_docker_image():
            print("\n✓ Docker image built successfully!")
        else:
            print("\n✗ Failed to build Docker image")
    
    elif choice == "2":
        print("\nStarting Jupyter Lab in Docker...")
        print("Access at: http://localhost:8888")
        print("Token: mt5password")
        subprocess.run(["docker-compose", "up"])
    
    elif choice == "3":
        print("\nStarting Docker container shell...")
        subprocess.run(["docker-compose", "exec", "mt5", "bash"])
    
    elif choice == "4":
        print("\n" + open("DOCKER_SETUP.md").read())
    
    elif choice == "5":
        print("Exiting...")
        sys.exit(0)
    
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
