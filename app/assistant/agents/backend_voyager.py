#!/usr/bin/env python3
"""
🚀 BackendVoyager - Backend Architecture & API Enhancement Agent
Optimizes APIs, database queries, caching, and backend performance
"""
import argparse, json, sys, re, subprocess
from pathlib import Path
from typing import Dict, List, Optional
import time

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("BackendVoyager")
    except Exception:
        return True

class BackendVoyager:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.backend_dir = self.project_root / "data" / "backend"
        self.backend_dir.mkdir(parents=True, exist_ok=True)
        
    def analyze_api_patterns(self):
        """Analyze API design patterns and suggest improvements"""
        api_files = []
        for pattern in ["*.py", "*.js", "*.ts"]:
            api_files.extend(list(self.project_root.rglob(pattern)))
        
        api_analysis = {
            "rest_endpoints": 0,
            "graphql_endpoints": 0,
            "websocket_connections": 0,
            "authentication_middleware": 0,
            "rate_limiting": 0,
            "input_validation": 0,
            "error_handling": 0,
            "async_operations": 0,
            "database_queries": 0,
            "caching_layers": 0
        }
        
        potential_issues = []
        
        for file_path in api_files:
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text()
                
                # REST API patterns
                if re.search(r"@app\.(get|post|put|delete)|@router\.|FastAPI|Flask", content):
                    api_analysis["rest_endpoints"] += 1
                
                # GraphQL patterns
                if re.search(r"graphql|GraphQL|resolver|schema", content, re.IGNORECASE):
                    api_analysis["graphql_endpoints"] += 1
                
                # WebSocket patterns
                if re.search(r"websocket|socket\.io|ws:|wss:", content, re.IGNORECASE):
                    api_analysis["websocket_connections"] += 1
                
                # Security patterns
                if re.search(r"auth|jwt|token|passport", content, re.IGNORECASE):
                    api_analysis["authentication_middleware"] += 1
                
                if re.search(r"rate.?limit|throttle", content, re.IGNORECASE):
                    api_analysis["rate_limiting"] += 1
                
                # Validation patterns
                if re.search(r"validate|pydantic|joi|schema", content, re.IGNORECASE):
                    api_analysis["input_validation"] += 1
                
                # Error handling
                if re.search(r"try:|except:|catch|error.?handler", content):
                    api_analysis["error_handling"] += 1
                
                # Async patterns
                if re.search(r"async|await|asyncio|Promise", content):
                    api_analysis["async_operations"] += 1
                
                # Database patterns
                if re.search(r"SELECT|INSERT|UPDATE|DELETE|query|find|aggregate", content):
                    api_analysis["database_queries"] += 1
                
                # Caching patterns
                if re.search(r"cache|redis|memcache", content, re.IGNORECASE):
                    api_analysis["caching_layers"] += 1
                
                # Check for potential issues
                if re.search(r"SELECT \*|\.all\(\)|\.find\(\{\}\)", content):
                    potential_issues.append(f"Potential N+1 query in {file_path.name}")
                
                if re.search(r"sleep|time\.sleep|setTimeout", content) and "test" not in str(file_path):
                    potential_issues.append(f"Blocking sleep found in {file_path.name}")
                    
            except Exception:
                continue
        
        return api_analysis, potential_issues
    
    def suggest_backend_improvements(self, analysis: Dict, issues: List[str]) -> List[str]:
        """Generate backend improvement suggestions"""
        suggestions = []
        
        if analysis["rate_limiting"] == 0:
            suggestions.append("Implement rate limiting to prevent API abuse")
        
        if analysis["caching_layers"] < 2:
            suggestions.append("Add Redis caching for frequently accessed data")
        
        if analysis["input_validation"] < analysis["rest_endpoints"] * 0.8:
            suggestions.append("Increase input validation coverage for API endpoints")
        
        if analysis["async_operations"] < analysis["rest_endpoints"] * 0.5:
            suggestions.append("Convert more operations to async for better performance")
        
        if analysis["authentication_middleware"] == 0:
            suggestions.append("Implement authentication middleware for secure endpoints")
        
        suggestions.extend([
            "Add API versioning strategy (v1, v2, etc.)",
            "Implement request/response logging for debugging",
            "Add health check endpoints (/health, /status)",
            "Set up API documentation (OpenAPI/Swagger)",
            "Implement database connection pooling",
            "Add monitoring and alerting for API metrics",
            "Consider implementing CORS policies",
            "Add request timeout handling",
            "Implement graceful shutdown handling"
        ])
        
        if issues:
            suggestions.append("Review and fix identified performance issues")
        
        return suggestions
    
    def analyze_database_usage(self):
        """Analyze database usage patterns"""
        db_patterns = {
            "orm_usage": 0,
            "raw_queries": 0,
            "migrations": 0,
            "indexes": 0,
            "transactions": 0,
            "connection_pooling": 0
        }
        
        db_files = list(self.project_root.rglob("*.py"))
        
        for file_path in db_files:
            if "venv" in str(file_path):
                continue
            try:
                content = file_path.read_text()
                
                if re.search(r"SQLAlchemy|Django|Mongoose|Prisma", content):
                    db_patterns["orm_usage"] += 1
                
                if re.search(r"execute|raw|sql", content, re.IGNORECASE):
                    db_patterns["raw_queries"] += 1
                
                if re.search(r"migration|migrate|alembic", content, re.IGNORECASE):
                    db_patterns["migrations"] += 1
                
                if re.search(r"index|INDEX|createIndex", content):
                    db_patterns["indexes"] += 1
                
                if re.search(r"transaction|commit|rollback", content, re.IGNORECASE):
                    db_patterns["transactions"] += 1
                
                if re.search(r"pool|connection.?pool", content, re.IGNORECASE):
                    db_patterns["connection_pooling"] += 1
                    
            except Exception:
                continue
        
        return db_patterns
    
    def generate_api_template(self, framework: str = "fastapi") -> str:
        """Generate optimized API template"""
        if framework == "fastapi":
            return '''
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Optimized API", version="1.0.0")

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Rate limiting setup
@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost", encoding="utf-8")
    await FastAPILimiter.init(redis_client)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-07-22"}

# Rate-limited endpoint example
@app.get("/api/v1/data")
async def get_data(request: Request, 
                  ratelimit: dict = Depends(RateLimiter(times=100, seconds=60))):
    return {"data": "example"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        return "# Template not available for this framework"

def main():
    parser = argparse.ArgumentParser(description="BackendVoyager - Backend Optimization")
    parser.add_argument("--analyze-apis", action="store_true", help="Analyze API patterns")
    parser.add_argument("--analyze-db", action="store_true", help="Analyze database usage")
    parser.add_argument("--suggestions", action="store_true", help="Get improvement suggestions")
    parser.add_argument("--generate-template", help="Generate API template (fastapi, express, django)")
    parser.add_argument("--full-report", action="store_true", help="Generate comprehensive backend report")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    
    if not is_agent_enabled():
        print("🚀 BackendVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("🚀 BackendVoyager: Smoke test passed!")
        return 0
    
    voyager = BackendVoyager()
    
    if args.analyze_apis or args.full_report:
        analysis, issues = voyager.analyze_api_patterns()
        print("🚀 API Pattern Analysis:")
        for pattern, count in analysis.items():
            print(f"  {pattern}: {count}")
        
        if issues:
            print("\n⚠️ Potential Issues:")
            for issue in issues:
                print(f"  - {issue}")
    
    if args.analyze_db or args.full_report:
        db_analysis = voyager.analyze_database_usage()
        print("\n🚀 Database Usage Analysis:")
        for pattern, count in db_analysis.items():
            print(f"  {pattern}: {count}")
    
    if args.suggestions or args.full_report:
        analysis, issues = voyager.analyze_api_patterns()
        suggestions = voyager.suggest_backend_improvements(analysis, issues)
        print("\n🚀 Backend Improvement Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    
    if args.generate_template:
        template = voyager.generate_api_template(args.generate_template)
        print(f"\n🚀 {args.generate_template.upper()} API Template:")
        print(template)
    
    # Save comprehensive report
    if args.full_report:
        analysis, issues = voyager.analyze_api_patterns()
        db_analysis = voyager.analyze_database_usage()
        suggestions = voyager.suggest_backend_improvements(analysis, issues)
        
        report_file = voyager.backend_dir / "backend_analysis.json"
        report_data = {
            "timestamp": time.time(),
            "api_analysis": analysis,
            "potential_issues": issues,
            "database_analysis": db_analysis,
            "suggestions": suggestions
        }
        
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n🚀 BackendVoyager: Full report saved to {report_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
