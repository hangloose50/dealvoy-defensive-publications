#!/usr/bin/env python3
"""
Test Import Fixes - Dealvoy System Validation
Protected by USPTO #63/850,603
"""

import sys
import os
from pathlib import Path

def test_agent_imports():
    """Test all agent script imports"""
    print("Testing agent imports...")
    agent_path = Path('Dealvoy_Desktop_Release/agent_scripts')
    
    if not agent_path.exists():
        print("❌ Agent scripts directory not found")
        return False
    
    sys.path.insert(0, str(agent_path))
    success_count = 0
    total_count = 0
    
    for py_file in agent_path.glob('*.py'):
        if py_file.name != '__init__.py':
            total_count += 1
            try:
                module_name = py_file.stem
                exec(f'import {module_name}')
                print(f'✅ {module_name}: Import successful')
                success_count += 1
            except Exception as e:
                print(f'❌ {module_name}: {e}')
    
    print(f"Agent imports: {success_count}/{total_count} successful")
    return success_count == total_count

def test_core_dependencies():
    """Test core Python dependencies"""
    print("\nTesting core dependencies...")
    deps = ['json', 'datetime', 'logging', 'os', 'sys', 'pathlib']
    
    for dep in deps:
        try:
            exec(f'import {dep}')
            print(f'✅ {dep}: Available')
        except ImportError:
            print(f'❌ {dep}: Missing')

def main():
    print("Dealvoy Import Validation Test")
    print("=" * 40)
    
    test_core_dependencies()
    agent_result = test_agent_imports()
    
    print("\n" + "=" * 40)
    if agent_result:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
