"""
MORPHEUS-X Import Verification Script
Tests all imports to ensure the app will run without errors
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("\n" + "="*60)
print("MORPHEUS-X Import Verification")
print("="*60 + "\n")

tests_passed = 0
tests_failed = 0

def test_import(module_name: str, function_name: str = None):
    """Test importing a module or specific function."""
    global tests_passed, tests_failed
    
    try:
        if function_name:
            exec(f"from {module_name} import {function_name}")
            print(f"✅ {module_name}.{function_name}")
            tests_passed += 1
        else:
            exec(f"import {module_name}")
            print(f"✅ {module_name}")
            tests_passed += 1
    except Exception as e:
        print(f"❌ {module_name}.{function_name or ''}: {str(e)}")
        tests_failed += 1

# Test external packages
print("Testing External Packages...")
test_import("streamlit")
test_import("plotly.graph_objects")
test_import("plotly.express")
test_import("pandas")
test_import("pefile")

print("\nTesting MORPHEUS Core Modules...")
test_import("core.analyzer", "analyze_file")
test_import("core.risk_engine", "calculate_risk_score")
test_import("core.risk_engine", "get_risk_level")
test_import("core.behavior_predictor", "predict_behaviors")
test_import("core.mitre_mapper", "map_all_findings_to_mitre")
test_import("core.yara_generator", "generate_yara_rule")
test_import("core.yara_generator", "generate_combined_rule")
test_import("core.similarity_engine", "calculate_similarity")

print("\nTesting GUI Utilities...")
test_import("gui_utils", "VisualizationEngine")
test_import("gui_utils", "TableGenerator")
test_import("report_generator", "ReportGenerator")

# Summary
print("\n" + "="*60)
print(f"Tests Passed: {tests_passed}")
print(f"Tests Failed: {tests_failed}")
print("="*60 + "\n")

if tests_failed == 0:
    print("✅ All imports successful! Dashboard is ready to run.\n")
    print("Run the dashboard with:")
    print("  streamlit run app.py\n")
    sys.exit(0)
else:
    print("❌ Some imports failed. Please install missing packages:\n")
    print("  pip install -r requirements.txt\n")
    sys.exit(1)
