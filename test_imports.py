#!/usr/bin/env python3
"""
Test script to verify the application can start correctly
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly"""
    try:
        from src.presentation.app import app
        print("✓ App import successful")
        
        from src.infrastructure.config.settings import settings
        print("✓ Settings import successful")
        
        from src.infrastructure.database.connection import engine
        print("✓ Database connection import successful")
        
        print("✓ All imports successful!")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

if __name__ == "__main__":
    print("Testing application imports...")
    if test_imports():
        print("🎉 Application is ready for deployment!")
        sys.exit(0)
    else:
        print("❌ Application has import issues")
        sys.exit(1)
