#!/usr/bin/env python3
"""
Startup script for Render deployment
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error in {description}:")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    else:
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")

def main():
    print("Starting deployment process...")
    
    # Run database migrations
    run_command("alembic upgrade head", "Database migrations")
    
    # Get port from environment
    port = os.getenv("PORT", "8000")
    
    # Start the application
    print(f"Starting application on port {port}...")
    start_command = f"uvicorn main:app --host 0.0.0.0 --port {port}"
    os.system(start_command)

if __name__ == "__main__":
    main()
