#!/usr/bin/env python3
"""
Manual migration script for Render deployment
Run this after the app is deployed to set up the database
"""
import subprocess
import sys
import os

def run_migrations():
    """Run Alembic migrations"""
    try:
        print("Running database migrations...")
        result = subprocess.run(["alembic", "upgrade", "head"], 
                              capture_output=True, text=True, check=True)
        print("✅ Migrations completed successfully!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Migration failed:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Alembic not found. Make sure it's installed.")
        return False

if __name__ == "__main__":
    print("🚀 Running manual database setup...")
    if run_migrations():
        print("🎉 Database setup completed!")
    else:
        print("💥 Database setup failed!")
        sys.exit(1)
