#!/usr/bin/env python3
"""
Test All Agents - Comprehensive Agent Validation System  
Protected by USPTO #63/850,603
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

def analyze_agent_file(agent_file):
    """Analyze an agent file for content and structure"""
    agent_name = agent_file.stem
    
    try:
        # Read file content
        content = agent_file.read_text()
        
        if len(content.strip()) < 50:
            return {
                "status": "empty",
                "agent_name": agent_name,
                "file_size": len(content),
                "error": "File is empty or too small"
            }
        
        # Check for class definition
        lines = content.split('\n')
        class_found = False
        class_name = None
        
        for line in lines:
            if line.strip().startswith('class '):
                class_found = True
                class_name = line.split('class ')[1].split('(')[0].split(':')[0].strip()
                break
        
        if not class_found:
            return {
                "status": "no_class",
                "agent_name": agent_name,
                "error": "No class definition found"
            }
        
        # Try to import and test
        sys.path.insert(0, str(agent_file.parent))
        agent_module = __import__(agent_name)
        
        if hasattr(agent_module, class_name):
            agent_class = getattr(agent_module, class_name)
            agent_instance = agent_class()
            
            # Test run method
            if hasattr(agent_instance, 'run'):
                result = agent_instance.run({})
                return {
                    "status": "success",
                    "agent_name": agent_name,
                    "class_name": class_name,
                    "has_run_method": True,
                    "result_type": type(result).__name__
                }
            else:
                return {
                    "status": "no_run_method",
                    "agent_name": agent_name,
                    "class_name": class_name,
                    "error": "No run method found"
                }
        else:
            return {
                "status": "class_not_accessible",
                "agent_name": agent_name,
                "expected_class": class_name,
                "error": "Class found in code but not accessible"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "agent_name": agent_name,
            "error": str(e)
        }
    finally:
        # Clean up path
        if str(agent_file.parent) in sys.path:
            sys.path.remove(str(agent_file.parent))

def test_all_agents():
    """Test all agents with detailed analysis"""
    print("Dealvoy Agent Analysis & Test Suite")
    print("=" * 60)
    print(f"Analysis started: {datetime.now().isoformat()}")
    print()
    
    agent_scripts_path = Path('Dealvoy_Desktop_Release/agent_scripts')
    
    if not agent_scripts_path.exists():
        print("❌ Agent scripts directory not found!")
        return False
    
    # Get all Python files
    agent_files = list(agent_scripts_path.glob('*.py'))
    agent_files = [f for f in agent_files if f.name != '__init__.py']
    
    print(f"Found {len(agent_files)} agent files to analyze")
    print("-" * 60)
    
    results = []
    categories = {
        "success": [],
        "empty": [],
        "no_class": [],
        "no_run_method": [],
        "error": []
    }
    
    for agent_file in sorted(agent_files):
        result = analyze_agent_file(agent_file)
        results.append(result)
        
        status = result["status"]
        agent_name = result["agent_name"]
        
        if status == "success":
            print(f"✅ {agent_name}: Fully functional")
            categories["success"].append(agent_name)
        elif status == "empty":
            print(f"📝 {agent_name}: Empty file ({result.get('file_size', 0)} bytes)")
            categories["empty"].append(agent_name)
        elif status == "no_class":
            print(f"🏗️  {agent_name}: No class definition")
            categories["no_class"].append(agent_name)
        elif status == "no_run_method":
            print(f"⚠️  {agent_name}: Missing run() method")
            categories["no_run_method"].append(agent_name)
        else:
            print(f"❌ {agent_name}: {result.get('error', 'Unknown error')}")
            categories["error"].append(agent_name)
    
    print("-" * 60)
    print("ANALYSIS SUMMARY:")
    print(f"✅ Fully Functional: {len(categories['success'])}")
    print(f"📝 Empty Files: {len(categories['empty'])}")
    print(f"🏗️  Missing Class: {len(categories['no_class'])}")
    print(f"⚠️  Missing run(): {len(categories['no_run_method'])}")
    print(f"❌ Errors: {len(categories['error'])}")
    print(f"📊 Total: {len(agent_files)}")
    
    if categories["success"]:
        print(f"\n✅ WORKING AGENTS ({len(categories['success'])}):")
        for agent in categories["success"]:
            print(f"   • {agent}")
    
    if categories["empty"]:
        print(f"\n📝 EMPTY FILES NEEDING CONTENT ({len(categories['empty'])}):")
        for agent in categories["empty"][:10]:  # Show first 10
            print(f"   • {agent}")
        if len(categories["empty"]) > 10:
            print(f"   ... and {len(categories['empty']) - 10} more")
    
    # Save detailed report
    report = {
        "analysis_timestamp": datetime.now().isoformat(),
        "summary": {
            "total_agents": len(agent_files),
            "functional": len(categories["success"]),
            "empty": len(categories["empty"]),
            "missing_class": len(categories["no_class"]),
            "missing_run_method": len(categories["no_run_method"]),
            "errors": len(categories["error"])
        },
        "categories": categories,
        "detailed_results": results
    }
    
    with open("agent_analysis_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report: agent_analysis_report.json")
    
    functional_rate = (len(categories["success"]) / len(agent_files)) * 100
    print(f"🎯 Functional Rate: {functional_rate:.1f}%")
    
    return len(categories["success"]) > 0

if __name__ == "__main__":
    test_all_agents()
