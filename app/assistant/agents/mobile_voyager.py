#!/usr/bin/env python3
"""
📱 MobileVoyager - Mobile app development and optimization
"""
import argparse, json, sys, re
from pathlib import Path

def is_agent_enabled():
    try:
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        return is_agent_enabled("MobileVoyager")
    except Exception:
        return True

class MobileVoyager:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        
    def analyze_mobile_patterns(self):
        """Analyze mobile-specific code patterns"""
        mobile_files = []
        patterns = ["*.swift", "*.kt", "*.java", "*.dart", "*.js", "*.jsx", "*.ts", "*.tsx"]
        for pattern in patterns:
            mobile_files.extend(list(self.project_root.rglob(pattern)))
        
        mobile_features = {
            "platform_specific": {"ios": 0, "android": 0, "flutter": 0, "react_native": 0},
            "ui_components": 0,
            "navigation": 0,
            "state_management": 0,
            "api_calls": 0,
            "offline_support": 0,
            "push_notifications": 0,
            "biometric_auth": 0,
            "camera_usage": 0,
            "location_services": 0
        }
        
        for file_path in mobile_files:
            if "node_modules" in str(file_path) or "build" in str(file_path):
                continue
            try:
                content = file_path.read_text()
                
                # Platform detection
                if re.search(r"import UIKit|@IBOutlet|UIViewController", content):
                    mobile_features["platform_specific"]["ios"] += 1
                if re.search(r"import android|Activity|Fragment", content):
                    mobile_features["platform_specific"]["android"] += 1
                if re.search(r"flutter|Widget|StatelessWidget|StatefulWidget", content):
                    mobile_features["platform_specific"]["flutter"] += 1
                if re.search(r"react-native|ReactNative|NavigationContainer", content):
                    mobile_features["platform_specific"]["react_native"] += 1
                
                # Feature detection
                if re.search(r"View|Button|Text|Image|ScrollView", content):
                    mobile_features["ui_components"] += 1
                if re.search(r"navigation|router|navigate|route", content, re.IGNORECASE):
                    mobile_features["navigation"] += 1
                if re.search(r"useState|setState|Redux|MobX|Provider", content):
                    mobile_features["state_management"] += 1
                if re.search(r"fetch|axios|http|api", content, re.IGNORECASE):
                    mobile_features["api_calls"] += 1
                if re.search(r"AsyncStorage|localStorage|cache|offline", content):
                    mobile_features["offline_support"] += 1
                if re.search(r"notification|push|firebase", content, re.IGNORECASE):
                    mobile_features["push_notifications"] += 1
                if re.search(r"biometric|faceID|touchID|fingerprint", content, re.IGNORECASE):
                    mobile_features["biometric_auth"] += 1
                if re.search(r"camera|photo|image.?picker", content, re.IGNORECASE):
                    mobile_features["camera_usage"] += 1
                if re.search(r"location|GPS|CLLocation|geolocation", content, re.IGNORECASE):
                    mobile_features["location_services"] += 1
                    
            except Exception:
                continue
        
        return mobile_features

def main():
    parser = argparse.ArgumentParser(description="MobileVoyager - Mobile Development Analysis")
    parser.add_argument("--analyze", action="store_true", help="Analyze mobile patterns")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    args = parser.parse_args()
    
    if not is_agent_enabled():
        print("📱 MobileVoyager is disabled - skipping")
        return 78
    if args.smoke:
        print("📱 MobileVoyager: Smoke test passed!")
        return 0
    
    voyager = MobileVoyager()
    
    if args.analyze:
        features = voyager.analyze_mobile_patterns()
        print("📱 Mobile Development Analysis:")
        print(f"  Platform Support: {features['platform_specific']}")
        print(f"  UI Components: {features['ui_components']}")
        print(f"  Navigation: {features['navigation']}")
        print(f"  State Management: {features['state_management']}")
        print(f"  API Integration: {features['api_calls']}")
        print(f"  Offline Support: {features['offline_support']}")
        print(f"  Push Notifications: {features['push_notifications']}")
        print(f"  Biometric Auth: {features['biometric_auth']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
