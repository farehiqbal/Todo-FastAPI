#!/usr/bin/env python3
"""
Quick verification that the app can start
"""
import sys
import os

def verify_app():
    """Verify the app can be imported and started"""
    try:
        # Test the main entry point
        from main import app
        print("✅ Main app import successful")
        
        # Test settings
        from src.infrastructure.config.settings import settings
        print(f"✅ Settings loaded - Debug: {settings.debug}")
        
        return True
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Verifying application...")
    if verify_app():
        print("🎉 Application verification successful!")
    else:
        print("💥 Application verification failed!")
        sys.exit(1)
