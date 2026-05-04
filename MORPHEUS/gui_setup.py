"""
MORPHEUS-X GUI Setup and Cleanup Script
Prepares the environment for malware analysis with real data
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime


def cleanup_fake_data():
    """Remove test/fake data generated during development."""
    
    print("🧹 MORPHEUS-X Cleanup Utility")
    print("=" * 60)
    print("This script removes test/fake data to prepare for real malware analysis.\n")
    
    cleanup_items = []
    
    # 1. Check for test data files
    print("Checking for test data files...")
    
    test_files = [
        "tests/test_behavior.py",
        "tests/test_detection.py", 
        "tests/test_static.py",
        "test_analyzer.py",
        "test_detection_engine.py",
        "test_intelligence_engine.py",
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            cleanup_items.append(("test_file", test_file))
            print(f"  ✓ Found test file: {test_file}")
    
    # 2. Check for fake data in rules directory
    print("\nChecking for demo rules...")
    demo_rules = []
    if os.path.exists("rules"):
        for file in os.listdir("rules"):
            if "demo" in file.lower() or "example" in file.lower():
                demo_rules.append(f"rules/{file}")
                print(f"  ✓ Found demo rule: {file}")
    
    if demo_rules:
        cleanup_items.extend([("demo_rule", rule) for rule in demo_rules])
    
    # 3. Check for fake data in docs
    print("\nChecking for sample outputs...")
    if os.path.exists("docs/sample_output.json"):
        cleanup_items.append(("sample_file", "docs/sample_output.json"))
        print("  ✓ Found sample output file")
    
    # 4. Check for temporary files
    print("\nChecking for temporary files...")
    temp_files = []
    for file in os.listdir("."):
        if file.startswith("temp_") or file.startswith(".temp_"):
            temp_files.append(file)
            print(f"  ✓ Found temporary file: {file}")
    
    if temp_files:
        cleanup_items.extend([("temp_file", file) for file in temp_files])
    
    # Summary
    print("\n" + "=" * 60)
    print(f"\nFound {len(cleanup_items)} items to clean up:")
    
    for item_type, item_name in cleanup_items:
        type_icon = {
            "test_file": "📝",
            "demo_rule": "🎯",
            "sample_file": "📊",
            "temp_file": "🗑️",
        }.get(item_type, "📦")
        print(f"  {type_icon} {item_name}")
    
    if not cleanup_items:
        print("  No test data found. System is ready for real malware analysis.")
        return
    
    # Confirm
    print("\n" + "=" * 60)
    response = input("\nProceed with cleanup? (yes/no): ").strip().lower()
    
    if response not in ["yes", "y"]:
        print("❌ Cleanup cancelled.")
        return
    
    # Perform cleanup
    print("\n🧹 Cleaning up...\n")
    
    removed_count = 0
    failed_count = 0
    
    for item_type, item_name in cleanup_items:
        try:
            if os.path.isfile(item_name):
                os.remove(item_name)
                print(f"  ✓ Removed: {item_name}")
            elif os.path.isdir(item_name):
                shutil.rmtree(item_name)
                print(f"  ✓ Removed directory: {item_name}")
            removed_count += 1
        except Exception as e:
            print(f"  ✗ Failed to remove {item_name}: {str(e)}")
            failed_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"\n✅ Cleanup completed!")
    print(f"   Removed: {removed_count} items")
    if failed_count > 0:
        print(f"   Failed: {failed_count} items")
    
    print("\n📋 Next steps:")
    print("   1. Prepare your malware samples (PE files)")
    print("   2. Place samples in appropriate location")
    print("   3. Run: streamlit run app.py")
    print("   4. Upload files through the GUI")
    print("\n⚠️  WARNING: Only analyze malware in isolated environments!")
    print("=" * 60)


def setup_directories():
    """Create necessary directories for the application."""
    
    print("\n📁 Setting up directories...\n")
    
    directories = [
        "data",
        "data/uploads",
        "data/analysis_results",
        "data/reports",
        "rules/generated",
        "logs",
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created/verified: {directory}")
        except Exception as e:
            print(f"  ✗ Failed to create {directory}: {str(e)}")
    
    print("\n✅ Directory setup completed!")


def verify_installation():
    """Verify all required packages are installed."""
    
    print("\n🔍 Verifying installation...\n")
    
    required_packages = [
        ("pefile", "pefile"),
        ("streamlit", "streamlit"),
        ("plotly", "plotly"),
        ("pandas", "pandas"),
        ("reportlab", "reportlab"),
        ("PIL", "pillow"),
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✓ {package_name} is installed")
        except ImportError:
            print(f"  ✗ {package_name} is NOT installed")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("\nInstall with:")
        print(f"   pip install {' '.join(missing_packages)}")
    else:
        print("\n✅ All required packages are installed!")
    
    return len(missing_packages) == 0


def create_config_file():
    """Create configuration file for the application."""
    
    print("\n⚙️  Creating configuration...\n")
    
    config = {
        "app_name": "MORPHEUS-X",
        "version": "1.0.0",
        "created": datetime.now().isoformat(),
        "settings": {
            "max_file_size_mb": 200,
            "analysis_timeout_seconds": 300,
            "enable_gpu": False,
            "storage_backend": "local",
        },
        "paths": {
            "uploads": "data/uploads",
            "results": "data/analysis_results",
            "reports": "data/reports",
            "rules": "rules/generated",
            "logs": "logs",
        }
    }
    
    try:
        with open("gui_config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("  ✓ Created gui_config.json")
    except Exception as e:
        print(f"  ✗ Failed to create config: {str(e)}")
    
    print("\n✅ Configuration created!")


def main():
    """Main setup function."""
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  MORPHEUS-X GUI Setup & Cleanup Tool".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    print("\nOptions:")
    print("  1. Clean up test data (prepare for real malware)")
    print("  2. Setup directories")
    print("  3. Verify installation")
    print("  4. Create configuration")
    print("  5. Run all setup steps")
    print("  6. Exit")
    
    choice = input("\nSelect option (1-6): ").strip()
    
    if choice == "1":
        cleanup_fake_data()
    elif choice == "2":
        setup_directories()
    elif choice == "3":
        verify_installation()
    elif choice == "4":
        create_config_file()
    elif choice == "5":
        print("\n▶️  Running full setup...\n")
        setup_directories()
        verify_installation()
        create_config_file()
        cleanup_fake_data()
    elif choice == "6":
        print("\nExiting. To start the GUI, run:")
        print("  streamlit run app.py")
    else:
        print("Invalid option. Please select 1-6.")


if __name__ == "__main__":
    main()
