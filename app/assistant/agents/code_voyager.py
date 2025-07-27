#!/usr/bin/env python3
"""
💻 CodeVoyager - Code Intelligence Agent
Analyzes, improves, and documents your codebase automatically
Provides deep code understanding for other Voyager agents
"""

import os
import ast
import json
import subprocess
from datetime import datetime
from pathlib import Path
import re

class CodeVoyager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.code_analysis_dir = self.project_path / "code_analysis"
        self.code_analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # Code analysis patterns
        self.code_patterns = {
            "complexity_indicators": [
                r"if.*elif.*else",
                r"for.*in.*:",
                r"while.*:",
                r"try.*except.*:",
                r"with.*as.*:"
            ],
            "code_smells": [
                r"def.*\(.*,.*,.*,.*,.*,.*,.*\)",  # Too many parameters
                r"class.*\(.*,.*,.*,.*\)",          # Multiple inheritance
                r"global\s+\w+",                    # Global variables
                r"#\s*TODO|#\s*FIXME|#\s*HACK"     # Technical debt markers
            ],
            "best_practices": [
                r"def.*\(.*\)\s*->.*:",             # Type hints
                r'""".*"""',                        # Docstrings
                r"import\s+\w+",                    # Clean imports
                r"if\s+__name__\s*==\s*['\"]__main__['\"]:"  # Main guard
            ]
        }
        
    def analyze_codebase_structure(self):
        """Map entire codebase structure and relationships"""
        print("💻 [CodeVoyager] Mapping project structure...")
        
        structure_map = {
            "timestamp": datetime.now().isoformat(),
            "project_stats": {
                "total_files": 0,
                "python_files": 0,
                "lines_of_code": 0,
                "functions": 0,
                "classes": 0,
                "imports": []
            },
            "modules": {},
            "dependencies": {},
            "quality_metrics": {}
        }
        
        # Scan all Python files
        for py_file in self.project_path.rglob("*.py"):
            if self._should_analyze_file(py_file):
                module_analysis = self._analyze_python_file(py_file)
                relative_path = str(py_file.relative_to(self.project_path))
                structure_map["modules"][relative_path] = module_analysis
                
                # Update global stats
                structure_map["project_stats"]["python_files"] += 1
                structure_map["project_stats"]["lines_of_code"] += module_analysis["lines_of_code"]
                structure_map["project_stats"]["functions"] += len(module_analysis["functions"])
                structure_map["project_stats"]["classes"] += len(module_analysis["classes"])
                structure_map["project_stats"]["imports"].extend(module_analysis["imports"])
                
        structure_map["project_stats"]["total_files"] = len(list(self.project_path.rglob("*")))
        structure_map["project_stats"]["imports"] = list(set(structure_map["project_stats"]["imports"]))
        
        return structure_map
    
    def _should_analyze_file(self, file_path):
        """Determine if file should be analyzed"""
        # Skip cache, build directories, and hidden files
        skip_patterns = ["__pycache__", ".git", "build", "dist", ".pytest_cache", "node_modules"]
        return not any(pattern in str(file_path) for pattern in skip_patterns)
    
    def _analyze_python_file(self, file_path):
        """Analyze individual Python file"""
        analysis = {
            "path": str(file_path),
            "lines_of_code": 0,
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity_score": 0,
            "quality_score": 0,
            "issues": [],
            "suggestions": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Basic metrics
            lines = content.split('\n')
            analysis["lines_of_code"] = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            
            # Parse AST for detailed analysis
            try:
                tree = ast.parse(content)
                analysis.update(self._analyze_ast(tree))
            except SyntaxError:
                analysis["issues"].append("Syntax error in file")
                
            # Pattern-based analysis
            analysis["complexity_score"] = self._calculate_complexity(content)
            analysis["quality_score"] = self._calculate_quality_score(content)
            analysis["issues"].extend(self._detect_code_issues(content))
            analysis["suggestions"].extend(self._generate_suggestions(content, analysis))
            
        except Exception as e:
            analysis["issues"].append(f"Analysis error: {str(e)}")
            
        return analysis
    
    def _analyze_ast(self, tree):
        """Analyze Python AST for functions, classes, and imports"""
        functions = []
        classes = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "args": len(node.args.args),
                    "has_docstring": ast.get_docstring(node) is not None,
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                    "line_number": node.lineno
                })
                
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                    "has_docstring": ast.get_docstring(node) is not None,
                    "bases": len(node.bases),
                    "line_number": node.lineno
                })
                
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                else:
                    module = node.module or ""
                    imports.extend([f"{module}.{alias.name}" for alias in node.names])
                    
        return {
            "functions": functions,
            "classes": classes,
            "imports": imports
        }
    
    def _calculate_complexity(self, content):
        """Calculate code complexity score"""
        complexity = 0
        
        for pattern_category, patterns in self.code_patterns.items():
            for pattern in patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                if pattern_category == "complexity_indicators":
                    complexity += matches * 2
                elif pattern_category == "code_smells":
                    complexity += matches * 5
                    
        return complexity
    
    def _calculate_quality_score(self, content):
        """Calculate code quality score (0-100)"""
        quality_points = 0
        total_possible = 100
        
        # Check for best practices
        for pattern in self.code_patterns["best_practices"]:
            if re.search(pattern, content):
                quality_points += 25
                
        # Penalize for code smells
        smell_count = 0
        for pattern in self.code_patterns["code_smells"]:
            smell_count += len(re.findall(pattern, content))
            
        quality_points -= smell_count * 10
        
        return max(0, min(100, quality_points))
    
    def _detect_code_issues(self, content):
        """Detect specific code issues"""
        issues = []
        
        # Check for long lines
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(f"Line {i}: Line too long ({len(line)} chars)")
                
        # Check for missing docstrings
        if '"""' not in content and "'''" not in content:
            if "def " in content or "class " in content:
                issues.append("Missing docstrings for functions/classes")
                
        # Check for unused imports (basic check)
        import_lines = [line for line in lines if line.strip().startswith(('import ', 'from '))]
        if len(import_lines) > 10:
            issues.append("High number of imports - consider refactoring")
            
        return issues
    
    def _generate_suggestions(self, content, analysis):
        """Generate improvement suggestions"""
        suggestions = []
        
        # Function-specific suggestions
        for func in analysis["functions"]:
            if not func["has_docstring"]:
                suggestions.append(f"Add docstring to function '{func['name']}'")
            if func["args"] > 5:
                suggestions.append(f"Function '{func['name']}' has many parameters - consider refactoring")
                
        # Class-specific suggestions
        for cls in analysis["classes"]:
            if not cls["has_docstring"]:
                suggestions.append(f"Add docstring to class '{cls['name']}'")
            if cls["methods"] > 15:
                suggestions.append(f"Class '{cls['name']}' is large - consider splitting")
                
        # Quality suggestions
        if analysis["quality_score"] < 50:
            suggestions.append("Consider improving code quality with better documentation and structure")
            
        if analysis["complexity_score"] > 50:
            suggestions.append("High complexity detected - consider refactoring for maintainability")
            
        return suggestions
    
    def generate_documentation(self, structure_map):
        """Auto-generate API documentation"""
        print("💻 [CodeVoyager] Generating documentation...")
        
        docs = {
            "project_overview": self._generate_project_overview(structure_map),
            "api_reference": self._generate_api_reference(structure_map),
            "module_index": self._generate_module_index(structure_map)
        }
        
        # Save markdown documentation
        docs_dir = self.code_analysis_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        
        # Project overview
        with open(docs_dir / "README.md", 'w') as f:
            f.write(docs["project_overview"])
            
        # API reference
        with open(docs_dir / "API.md", 'w') as f:
            f.write(docs["api_reference"])
            
        return docs
    
    def _generate_project_overview(self, structure_map):
        """Generate project overview documentation"""
        stats = structure_map["project_stats"]
        
        overview = f"""# Project Overview
Generated by CodeVoyager on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Statistics
- **Python Files**: {stats['python_files']}
- **Lines of Code**: {stats['lines_of_code']:,}
- **Functions**: {stats['functions']}
- **Classes**: {stats['classes']}
- **Dependencies**: {len(stats['imports'])}

## Key Modules
"""
        
        # Add top modules by complexity/size
        modules = list(structure_map["modules"].items())
        modules.sort(key=lambda x: x[1]["lines_of_code"], reverse=True)
        
        for module_path, module_data in modules[:10]:
            overview += f"\n### {module_path}\n"
            overview += f"- Lines: {module_data['lines_of_code']}\n"
            overview += f"- Functions: {len(module_data['functions'])}\n"
            overview += f"- Classes: {len(module_data['classes'])}\n"
            if module_data['issues']:
                overview += f"- Issues: {len(module_data['issues'])}\n"
                
        return overview
    
    def _generate_api_reference(self, structure_map):
        """Generate API reference documentation"""
        api_ref = f"""# API Reference
Generated by CodeVoyager on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        for module_path, module_data in structure_map["modules"].items():
            if module_data["classes"] or module_data["functions"]:
                api_ref += f"\n## {module_path}\n\n"
                
                # Document classes
                for cls in module_data["classes"]:
                    api_ref += f"### Class: {cls['name']}\n"
                    api_ref += f"- Methods: {cls['methods']}\n"
                    api_ref += f"- Line: {cls['line_number']}\n"
                    if not cls['has_docstring']:
                        api_ref += "- ⚠️ Missing docstring\n"
                    api_ref += "\n"
                    
                # Document functions
                for func in module_data["functions"]:
                    api_ref += f"### Function: {func['name']}\n"
                    api_ref += f"- Parameters: {func['args']}\n"
                    api_ref += f"- Line: {func['line_number']}\n"
                    if func['is_async']:
                        api_ref += "- Type: Async\n"
                    if not func['has_docstring']:
                        api_ref += "- ⚠️ Missing docstring\n"
                    api_ref += "\n"
                    
        return api_ref
    
    def _generate_module_index(self, structure_map):
        """Generate module index"""
        index = {}
        
        for module_path, module_data in structure_map["modules"].items():
            index[module_path] = {
                "summary": f"{len(module_data['functions'])} functions, {len(module_data['classes'])} classes",
                "quality_score": module_data["quality_score"],
                "complexity_score": module_data["complexity_score"],
                "needs_attention": len(module_data["issues"]) > 0
            }
            
        return index
    
    def suggest_refactors(self, structure_map):
        """Suggest code refactoring opportunities"""
        print("💻 [CodeVoyager] Analyzing refactoring opportunities...")
        
        refactor_suggestions = {
            "high_priority": [],
            "medium_priority": [],
            "low_priority": []
        }
        
        for module_path, module_data in structure_map["modules"].items():
            # High priority: files with many issues
            if len(module_data["issues"]) > 5:
                refactor_suggestions["high_priority"].append({
                    "file": module_path,
                    "reason": f"Multiple issues detected ({len(module_data['issues'])})",
                    "suggestions": module_data["suggestions"][:3]
                })
                
            # Medium priority: high complexity
            elif module_data["complexity_score"] > 50:
                refactor_suggestions["medium_priority"].append({
                    "file": module_path,
                    "reason": f"High complexity score ({module_data['complexity_score']})",
                    "suggestions": ["Consider breaking into smaller functions", "Add more documentation"]
                })
                
            # Low priority: quality improvements
            elif module_data["quality_score"] < 70:
                refactor_suggestions["low_priority"].append({
                    "file": module_path,
                    "reason": f"Quality score could be improved ({module_data['quality_score']}/100)",
                    "suggestions": ["Add docstrings", "Follow PEP 8 guidelines"]
                })
                
        return refactor_suggestions
    
    def run_code_formatters(self):
        """Run automated code formatting tools"""
        print("💻 [CodeVoyager] Running code formatters...")
        
        formatter_results = {
            "black": {"status": "not_available", "output": ""},
            "isort": {"status": "not_available", "output": ""},
            "flake8": {"status": "not_available", "output": ""}
        }
        
        # Try to run black (code formatter)
        try:
            result = subprocess.run(
                ["python3", "-m", "black", "--check", "--diff", str(self.project_path)],
                capture_output=True, text=True, timeout=30
            )
            formatter_results["black"] = {
                "status": "available" if result.returncode in [0, 1] else "error",
                "output": result.stdout[:500] if result.stdout else "No changes needed"
            }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            formatter_results["black"]["output"] = "Black not installed - run: pip install black"
            
        # Try to run isort (import sorter)
        try:
            result = subprocess.run(
                ["python3", "-m", "isort", "--check-only", "--diff", str(self.project_path)],
                capture_output=True, text=True, timeout=30
            )
            formatter_results["isort"] = {
                "status": "available" if result.returncode in [0, 1] else "error",
                "output": result.stdout[:500] if result.stdout else "Imports are sorted"
            }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            formatter_results["isort"]["output"] = "isort not installed - run: pip install isort"
            
        # Try to run flake8 (linter)
        try:
            result = subprocess.run(
                ["python3", "-m", "flake8", str(self.project_path)],
                capture_output=True, text=True, timeout=30
            )
            formatter_results["flake8"] = {
                "status": "available",
                "output": result.stdout[:500] if result.stdout else "No linting issues found"
            }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            formatter_results["flake8"]["output"] = "flake8 not installed - run: pip install flake8"
            
        return formatter_results
    
    def run(self):
        """Main execution function"""
        print("💻 [CodeVoyager] Scanning codebase for improvements...")
        
        # 1. Map project structure
        print("   📁 Mapping project structure...")
        structure_map = self.analyze_codebase_structure()
        
        # 2. Generate documentation
        print("   📄 Generating documentation...")
        documentation = self.generate_documentation(structure_map)
        
        # 3. Suggest refactors
        print("   🔧 Suggesting refactors and improvements...")
        refactor_suggestions = self.suggest_refactors(structure_map)
        
        # 4. Run formatters/linters
        print("   🎨 Running lint/format actions...")
        formatter_results = self.run_code_formatters()
        
        # 5. Save comprehensive analysis
        analysis_file = self.code_analysis_dir / f"code_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        comprehensive_analysis = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "voyager": "code_voyager",
                "version": "1.0.0"
            },
            "structure_map": structure_map,
            "refactor_suggestions": refactor_suggestions,
            "formatter_results": formatter_results,
            "summary": {
                "total_python_files": structure_map["project_stats"]["python_files"],
                "total_lines": structure_map["project_stats"]["lines_of_code"],
                "high_priority_refactors": len(refactor_suggestions["high_priority"]),
                "documentation_generated": True
            }
        }
        
        with open(analysis_file, 'w') as f:
            json.dump(comprehensive_analysis, f, indent=2)
            
        # Print results
        print("✅ CodeVoyager: Analysis complete!")
        print(f"   📊 Files Analyzed: {structure_map['project_stats']['python_files']}")
        print(f"   📝 Lines of Code: {structure_map['project_stats']['lines_of_code']:,}")
        print(f"   🔧 High Priority Refactors: {len(refactor_suggestions['high_priority'])}")
        print(f"   📄 Documentation: Generated in {self.code_analysis_dir}/docs/")
        print(f"   📊 Full Analysis: {analysis_file}")
        
        # Print top refactor suggestions
        if refactor_suggestions["high_priority"]:
            print("\n🚨 High Priority Refactors:")
            for suggestion in refactor_suggestions["high_priority"][:3]:
                print(f"   📁 {suggestion['file']}")
                print(f"      {suggestion['reason']}")
                
        # Print formatter status
        print("\n🎨 Code Formatting Status:")
        for tool, result in formatter_results.items():
            status_icon = "✅" if result["status"] == "available" else "❌"
            print(f"   {status_icon} {tool.title()}: {result['output'][:50]}...")
            
        print("💻 [CodeVoyager] Ready for continuous code improvement!")

def run():
    """CLI entry point"""
    voyager = CodeVoyager()
    voyager.run()

if __name__ == "__main__":
    run()
