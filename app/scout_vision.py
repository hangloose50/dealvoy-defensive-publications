#!/usr/bin/env python3
"""
📸 ScoutVision - Camera capture + OCR integration for real-time product detection
Combines camera feeds with Tesseract OCR for intelligent product scanning
"""

import os
import json
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
try:
    import pytesseract
    from PIL import Image
except ImportError:
    print("📸 [ScoutVision] Installing required packages...")
    print("   pip install pytesseract pillow opencv-python")

class ScoutVision:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.vision_dir = self.project_path / "scout_vision"
        self.vision_dir.mkdir(parents=True, exist_ok=True)
        
        # OCR Configuration
        self.tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789$.,%-'
        
        # Product detection patterns
        self.product_patterns = {
            "price": r'\$[\d,]+\.?\d*',
            "model": r'[A-Z0-9]{3,}-[A-Z0-9]{3,}',
            "brand": ['Apple', 'Samsung', 'Sony', 'LG', 'Microsoft', 'Amazon', 'Google'],
            "discount": r'\d+%\s*off',
            "upc": r'\d{12}',
            "sku": r'SKU[:\s]*[A-Z0-9]+',
            "asin": r'B[0-9A-Z]{9}'
        }
        
    def capture_from_camera(self, duration=10):
        """Capture frames from camera for specified duration"""
        print("📸 [ScoutVision] Starting camera capture...")
        
        cap = cv2.VideoCapture(0)  # Default camera
        if not cap.isOpened():
            print("❌ [ScoutVision] Could not open camera")
            return []
            
        frames = []
        start_time = datetime.now()
        frame_count = 0
        
        while (datetime.now() - start_time).seconds < duration:
            ret, frame = cap.read()
            if ret:
                # Capture every 30th frame (approximately 1 per second)
                if frame_count % 30 == 0:
                    frames.append(frame)
                    print(f"   📷 Captured frame {len(frames)}")
                frame_count += 1
            else:
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"✅ [ScoutVision] Captured {len(frames)} frames")
        return frames
    
    def preprocess_frame(self, frame):
        """Preprocess frame for optimal OCR"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text_from_frame(self, frame):
        """Extract text from frame using OCR"""
        try:
            # Preprocess frame
            processed_frame = self.preprocess_frame(frame)
            
            # Convert to PIL Image for Tesseract
            pil_image = Image.fromarray(processed_frame)
            
            # Extract text
            text = pytesseract.image_to_string(pil_image, config=self.tesseract_config)
            
            # Get bounding boxes for detected text
            boxes = pytesseract.image_to_boxes(pil_image, config=self.tesseract_config)
            
            return {
                "text": text.strip(),
                "boxes": boxes,
                "confidence": self._calculate_confidence(text)
            }
            
        except Exception as e:
            print(f"❌ [ScoutVision] OCR error: {e}")
            return {"text": "", "boxes": "", "confidence": 0.0}
    
    def _calculate_confidence(self, text):
        """Calculate confidence score for extracted text"""
        if not text:
            return 0.0
            
        # Simple confidence calculation based on text characteristics
        score = 0.0
        
        # Length bonus
        if len(text) > 10:
            score += 0.3
            
        # Contains digits (prices, models)
        if any(char.isdigit() for char in text):
            score += 0.2
            
        # Contains currency symbols
        if '$' in text or '€' in text or '£' in text:
            score += 0.3
            
        # Contains brand names
        for brand in self.product_patterns['brand']:
            if brand.lower() in text.lower():
                score += 0.2
                break
                
        return min(score, 1.0)
    
    def analyze_product_info(self, ocr_result):
        """Analyze OCR result for product information"""
        text = ocr_result["text"]
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "raw_text": text,
            "detected_info": {},
            "confidence": ocr_result["confidence"],
            "suggestions": []
        }
        
        # Extract prices
        import re
        prices = re.findall(self.product_patterns["price"], text)
        if prices:
            analysis["detected_info"]["prices"] = prices
            analysis["suggestions"].append("Price detected - ready for comparison")
            
        # Extract model numbers
        models = re.findall(self.product_patterns["model"], text)
        if models:
            analysis["detected_info"]["models"] = models
            analysis["suggestions"].append("Model number found - search for reviews")
            
        # Extract discounts
        discounts = re.findall(self.product_patterns["discount"], text)
        if discounts:
            analysis["detected_info"]["discounts"] = discounts
            analysis["suggestions"].append("Discount detected - compare with regular price")
            
        # Extract UPC/SKU/ASIN
        for pattern_name, pattern in [("upc", "upc"), ("sku", "sku"), ("asin", "asin")]:
            matches = re.findall(self.product_patterns[pattern], text, re.IGNORECASE)
            if matches:
                analysis["detected_info"][pattern_name] = matches
                analysis["suggestions"].append(f"{pattern_name.upper()} found - lookup product details")
                
        # Detect brands
        detected_brands = []
        for brand in self.product_patterns['brand']:
            if brand.lower() in text.lower():
                detected_brands.append(brand)
        
        if detected_brands:
            analysis["detected_info"]["brands"] = detected_brands
            analysis["suggestions"].append("Brand identified - check brand-specific deals")
            
        return analysis
    
    def scan_real_time(self, duration=30):
        """Real-time scanning with live analysis"""
        print("📸 [ScoutVision] Starting real-time product scanning...")
        print(f"   ⏱️  Scanning for {duration} seconds")
        print("   📱 Point camera at products, prices, or labels")
        
        # Capture frames
        frames = self.capture_from_camera(duration)
        
        if not frames:
            print("❌ [ScoutVision] No frames captured")
            return None
            
        # Analyze each frame
        scan_results = []
        
        for i, frame in enumerate(frames):
            print(f"🔍 [ScoutVision] Analyzing frame {i+1}/{len(frames)}...")
            
            # Extract text
            ocr_result = self.extract_text_from_frame(frame)
            
            if ocr_result["text"]:
                # Analyze product information
                analysis = self.analyze_product_info(ocr_result)
                
                # Save frame if we found something interesting
                if analysis["detected_info"]:
                    frame_path = self.vision_dir / f"scan_frame_{i+1}_{datetime.now().strftime('%H%M%S')}.jpg"
                    cv2.imwrite(str(frame_path), frame)
                    analysis["frame_path"] = str(frame_path)
                    
                scan_results.append(analysis)
                
        # Generate comprehensive report
        report = self._generate_scan_report(scan_results)
        
        # Save report
        report_path = self.vision_dir / f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"✅ [ScoutVision] Scan complete! Report: {report_path}")
        return report
    
    def _generate_scan_report(self, scan_results):
        """Generate comprehensive scan report"""
        report = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_frames_analyzed": len(scan_results),
            "frames_with_text": len([r for r in scan_results if r["raw_text"]]),
            "frames_with_products": len([r for r in scan_results if r["detected_info"]]),
            "summary": {
                "all_prices": [],
                "all_brands": [],
                "all_models": [],
                "all_discounts": []
            },
            "detailed_results": scan_results,
            "recommendations": []
        }
        
        # Aggregate findings
        for result in scan_results:
            info = result["detected_info"]
            
            if "prices" in info:
                report["summary"]["all_prices"].extend(info["prices"])
            if "brands" in info:
                report["summary"]["all_brands"].extend(info["brands"])
            if "models" in info:
                report["summary"]["all_models"].extend(info["models"])
            if "discounts" in info:
                report["summary"]["all_discounts"].extend(info["discounts"])
                
        # Remove duplicates
        for key in report["summary"]:
            report["summary"][key] = list(set(report["summary"][key]))
            
        # Generate recommendations
        if report["summary"]["all_prices"]:
            report["recommendations"].append("💰 Prices detected - run price comparison analysis")
            
        if report["summary"]["all_brands"]:
            brands = ", ".join(report["summary"]["all_brands"])
            report["recommendations"].append(f"🏷️  Brands found: {brands} - check for brand-specific promotions")
            
        if report["summary"]["all_discounts"]:
            report["recommendations"].append("🔥 Discounts detected - verify against regular pricing")
            
        if not report["frames_with_products"]:
            report["recommendations"].append("💡 No products detected - try better lighting or closer positioning")
            
        return report
    
    def run(self):
        """Main execution function"""
        print("📸 [ScoutVision] Camera + OCR Product Scanner")
        print("   🎯 Real-time product detection and analysis")
        
        # Check dependencies
        try:
            import pytesseract
            print("✅ [ScoutVision] Tesseract OCR available")
        except ImportError:
            print("❌ [ScoutVision] Please install: pip install pytesseract pillow opencv-python")
            return
            
        # Run real-time scan
        report = self.scan_real_time(duration=15)
        
        if report:
            print("\n📊 [ScoutVision] Scan Summary:")
            print(f"   📱 Frames analyzed: {report['total_frames_analyzed']}")
            print(f"   📝 Frames with text: {report['frames_with_text']}")
            print(f"   🎯 Frames with products: {report['frames_with_products']}")
            
            if report["summary"]["all_prices"]:
                prices = ", ".join(report["summary"]["all_prices"])
                print(f"   💰 Prices found: {prices}")
                
            if report["summary"]["all_brands"]:
                brands = ", ".join(report["summary"]["all_brands"])
                print(f"   🏷️  Brands found: {brands}")
                
            print("\n💡 [ScoutVision] Recommendations:")
            for rec in report["recommendations"]:
                print(f"   {rec}")
                
        print("\n📸 [ScoutVision] Ready for continuous product scanning!")

def run():
    """CLI entry point"""
    scout = ScoutVision()
    scout.run()

if __name__ == "__main__":
    run()
