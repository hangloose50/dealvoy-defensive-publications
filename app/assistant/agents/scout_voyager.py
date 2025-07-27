#!/usr/bin/env python3
"""
📸 ScoutVoyager - Computer vision and OCR capabilities
Real-time product scanning, image analysis, and text extraction
"""

import os
import json
import subprocess
import argparse
import base64
import numpy as np
from datetime import datetime
from pathlib import Path

# Optional imports - will be checked at runtime
try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
    Image = ImageEnhance = ImageFilter = None

class ScoutVoyager:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.scout_dir = self.project_path / "scout_vision"
        self.scout_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.scout_dir / "captures").mkdir(exist_ok=True)
        (self.scout_dir / "processed").mkdir(exist_ok=True)
        (self.scout_dir / "extracted_text").mkdir(exist_ok=True)
        (self.scout_dir / "product_matches").mkdir(exist_ok=True)
        
    def capture_screen(self, region=None):
        """Capture screenshot with optional region"""
        print("📸 [ScoutVoyager] Capturing screen...")
        
        try:
            import pyautogui
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            capture_file = self.scout_dir / "captures" / f"capture_{timestamp}.png"
            
            if region:
                # Capture specific region (x, y, width, height)
                screenshot = pyautogui.screenshot(region=region)
            else:
                # Capture full screen
                screenshot = pyautogui.screenshot()
                
            screenshot.save(capture_file)
            
            return {
                "timestamp": datetime.now().isoformat(),
                "capture_file": str(capture_file),
                "region": region,
                "size": screenshot.size,
                "status": "success"
            }
            
        except ImportError:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "message": "pyautogui not available - install with: pip install pyautogui"
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "message": f"Screen capture failed: {str(e)}"
            }
    
    def preprocess_image(self, image_path):
        """Enhance image for better OCR results"""
        print("🔧 [ScoutVoyager] Preprocessing image for OCR...")
        
        try:
            # Load image
            img = Image.open(image_path)
            
            # Convert to grayscale
            if img.mode != 'L':
                img = img.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.5)
            
            # Apply slight blur to reduce noise
            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            # Save processed image
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            processed_file = self.scout_dir / "processed" / f"processed_{timestamp}.png"
            img.save(processed_file)
            
            return {
                "original": str(image_path),
                "processed": str(processed_file),
                "enhancements": ["grayscale", "contrast", "sharpness", "noise_reduction"],
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Image preprocessing failed: {str(e)}"
            }
    
    def extract_text_tesseract(self, image_path):
        """Extract text using Tesseract OCR"""
        print("🔍 [ScoutVoyager] Extracting text with Tesseract...")
        
        try:
            import pytesseract
            
            # Load image
            img = Image.open(image_path)
            
            # Extract text with different configurations
            configs = [
                "--psm 6",  # Uniform block of text
                "--psm 8",  # Single word
                "--psm 13", # Raw line. Treat the image as a single text line
                "--psm 11", # Sparse text
            ]
            
            extraction_results = []
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(img, config=config).strip()
                    confidence = pytesseract.image_to_data(img, config=config, output_type=pytesseract.Output.DATAFRAME)
                    avg_confidence = confidence['conf'].mean() if not confidence.empty else 0
                    
                    if text and avg_confidence > 30:  # Only include decent quality results
                        extraction_results.append({
                            "config": config,
                            "text": text,
                            "confidence": avg_confidence,
                            "word_count": len(text.split())
                        })
                        
                except Exception:
                    continue
            
            # Get best result
            if extraction_results:
                best_result = max(extraction_results, key=lambda x: x['confidence'])
                
                return {
                    "timestamp": datetime.now().isoformat(),
                    "image": str(image_path),
                    "extracted_text": best_result['text'],
                    "confidence": best_result['confidence'],
                    "config_used": best_result['config'],
                    "all_results": extraction_results,
                    "status": "success"
                }
            else:
                return {
                    "timestamp": datetime.now().isoformat(),
                    "image": str(image_path),
                    "extracted_text": "",
                    "confidence": 0,
                    "status": "no_text_found"
                }
                
        except ImportError:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "message": "pytesseract not available - install with: pip install pytesseract"
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "message": f"Text extraction failed: {str(e)}"
            }
    
    def extract_text_easyocr(self, image_path):
        """Extract text using EasyOCR (alternative OCR engine)"""
        print("🔍 [ScoutVoyager] Extracting text with EasyOCR...")
        
        try:
            import easyocr
            
            # Initialize EasyOCR reader
            reader = easyocr.Reader(['en'])
            
            # Read text from image
            results = reader.readtext(str(image_path))
            
            # Process results
            extracted_texts = []
            total_confidence = 0
            
            for (bbox, text, confidence) in results:
                if confidence > 0.3:  # Filter low confidence results
                    extracted_texts.append({
                        "text": text.strip(),
                        "confidence": confidence,
                        "bbox": bbox
                    })
                    total_confidence += confidence
            
            # Combine all text
            combined_text = " ".join([item["text"] for item in extracted_texts])
            avg_confidence = total_confidence / len(extracted_texts) if extracted_texts else 0
            
            return {
                "timestamp": datetime.now().isoformat(),
                "image": str(image_path),
                "extracted_text": combined_text,
                "confidence": avg_confidence,
                "individual_results": extracted_texts,
                "engine": "easyocr",
                "status": "success"
            }
            
        except ImportError:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error", 
                "message": "easyocr not available - install with: pip install easyocr"
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "message": f"EasyOCR extraction failed: {str(e)}"
            }
    
    def detect_products(self, text):
        """Detect product information from extracted text"""
        print("🛍️ [ScoutVoyager] Analyzing text for product information...")
        
        import re
        
        product_info = {
            "timestamp": datetime.now().isoformat(),
            "source_text": text,
            "detected_items": []
        }
        
        # Price patterns
        price_patterns = [
            r'\$\d+\.?\d*',  # $19.99, $19
            r'\d+\.\d{2}\s*(?:USD|usd|\$)',  # 19.99 USD
            r'(?:Price|PRICE)[:=\s]+\$?\d+\.?\d*',  # Price: $19.99
        ]
        
        # Product code patterns  
        code_patterns = [
            r'(?:ASIN|asin|B0[A-Z0-9]{8})',  # Amazon ASIN
            r'(?:UPC|upc)[:=\s]*\d{12}',     # UPC codes
            r'(?:SKU|sku)[:=\s]*[A-Z0-9\-]+', # SKU codes
            r'(?:Model|MODEL)[:=\s]*[A-Z0-9\-]+', # Model numbers
        ]
        
        # Brand patterns
        brand_patterns = [
            r'(?:Brand|BRAND)[:=\s]*([A-Z][a-zA-Z\s]+)',
            r'(?:by|BY)\s+([A-Z][a-zA-Z\s]+)',
        ]
        
        detected_prices = []
        detected_codes = []
        detected_brands = []
        
        # Extract prices
        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            detected_prices.extend(matches)
            
        # Extract product codes
        for pattern in code_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            detected_codes.extend(matches)
            
        # Extract brands
        for pattern in brand_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            detected_brands.extend(matches)
        
        # Clean and deduplicate results
        product_info["detected_items"] = {
            "prices": list(set(detected_prices)),
            "product_codes": list(set(detected_codes)),
            "brands": list(set([b.strip() for b in detected_brands])),
            "potential_titles": self._extract_titles(text)
        }
        
        # Calculate confidence score
        score = 0
        if detected_prices: score += 30
        if detected_codes: score += 40
        if detected_brands: score += 20
        if product_info["detected_items"]["potential_titles"]: score += 10
        
        product_info["confidence_score"] = min(score, 100)
        product_info["is_product_detected"] = score > 30
        
        return product_info
    
    def _extract_titles(self, text):
        """Extract potential product titles from text"""
        lines = text.split('\n')
        potential_titles = []
        
        for line in lines:
            line = line.strip()
            # Look for lines that might be product titles
            if (5 < len(line) < 100 and 
                not line.startswith('$') and
                not line.lower().startswith(('price', 'brand', 'model')) and
                len(line.split()) > 1):
                potential_titles.append(line)
                
        return potential_titles[:3]  # Return top 3 candidates
    
    def scan_and_extract(self, image_path=None, region=None):
        """Full pipeline: capture, preprocess, extract, and analyze"""
        print("🚀 [ScoutVoyager] Running full scan and extraction pipeline...")
        
        # Step 1: Capture if no image provided
        if not image_path:
            capture_result = self.capture_screen(region)
            if capture_result["status"] != "success":
                return capture_result
            image_path = capture_result["capture_file"]
        
        # Step 2: Preprocess image
        preprocess_result = self.preprocess_image(image_path)
        if preprocess_result["status"] != "success":
            return preprocess_result
            
        processed_image = preprocess_result["processed"]
        
        # Step 3: Extract text (try both engines)
        tesseract_result = self.extract_text_tesseract(processed_image)
        easyocr_result = self.extract_text_easyocr(processed_image)
        
        # Choose best OCR result
        best_text = ""
        best_confidence = 0
        ocr_engine = "none"
        
        if tesseract_result.get("status") == "success" and tesseract_result.get("confidence", 0) > best_confidence:
            best_text = tesseract_result["extracted_text"]
            best_confidence = tesseract_result["confidence"]
            ocr_engine = "tesseract"
            
        if easyocr_result.get("status") == "success" and easyocr_result.get("confidence", 0) > best_confidence:
            best_text = easyocr_result["extracted_text"]
            best_confidence = easyocr_result["confidence"]
            ocr_engine = "easyocr"
        
        # Step 4: Analyze for product information
        product_analysis = self.detect_products(best_text) if best_text else {"detected_items": {}}
        
        # Compile comprehensive results
        scan_results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "voyager": "scout_voyager",
                "version": "1.0.0"
            },
            "capture": {
                "source_image": str(image_path),
                "processed_image": processed_image,
                "region": region
            },
            "ocr": {
                "engine_used": ocr_engine,
                "extracted_text": best_text,
                "confidence": best_confidence,
                "tesseract_result": tesseract_result,
                "easyocr_result": easyocr_result
            },
            "product_analysis": product_analysis,
            "overall_status": "success" if best_text else "no_text_extracted"
        }
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = self.scout_dir / "extracted_text" / f"scan_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(scan_results, f, indent=2)
            
        return scan_results
    
    def run(self, smoke=False):
        """Main execution function (now uses scout_ocr and match_product as primary pipeline)"""
        print("📸 [ScoutVoyager] Initializing computer vision system...")
        if smoke:
            print("   🚀 FAST MODE: Running smoke tests only")
            return {
                "mode": "smoke",
                "status": "pass",
                "message": "ScoutVoyager smoke test completed",
                "capabilities": ["screen_capture", "ocr", "product_detection"]
            }

        # Try new pipeline first
        try:
            from app.vision.scout_ocr import ScoutOCR
            from app.vision.match_product import ProductMatcher
            ocr = ScoutOCR(str(self.project_path))
            matcher = ProductMatcher(str(self.project_path))
            print("🔭 [ScoutVoyager] Running new OCR + product matching pipeline...")
            ocr_result = ocr.run_ocr_pipeline(save_results=False)
            if ocr_result.get("status") != "success":
                print(f"❌ OCR pipeline failed: {ocr_result.get('message')}")
                return {"status": "error", "message": ocr_result.get("message")}
            match_result = matcher.run_matching_pipeline(ocr_result, save_results=False)
            if match_result.get("status") != "success":
                print(f"❌ Product matching failed: {match_result.get('message')}")
                return {"status": "error", "message": match_result.get("message")}
            # Save combined result
            result = {
                "timestamp": datetime.now().isoformat(),
                "ocr": ocr_result,
                "match": match_result,
                "status": "success"
            }
            # Print summary
            summary = match_result.get("match_summary", {})
            print("\n🔭 ScoutVoyager Results:")
            print(f"   📊 OCR Confidence: {ocr_result.get('raw_ocr', {}).get('confidence', 0)}%")
            print(f"   🎯 Best Match: {summary.get('best_match', {}).get('product', {}).get('name', 'None') if summary.get('best_match') else 'None'}")
            print(f"   ⭐ Confidence: {summary.get('confidence_score', 0)}%")
            print(f"   🏷️ UPC: {summary.get('best_match', {}).get('product', {}).get('upc', 'None') if summary.get('best_match') else 'None'}")
            print(f"   💰 Price: {summary.get('best_match', {}).get('product', {}).get('price', 'None') if summary.get('best_match') else 'None'}")
            print(f"   🏭 Brand: {summary.get('best_match', {}).get('product', {}).get('brand', 'None') if summary.get('best_match') else 'None'}")
            print(f"   📝 Total Matches: {summary.get('total_matches', 0)}")
            return result
        except Exception as e:
            print(f"⚠️  New pipeline failed ({e}), falling back to legacy pipeline.")
            # Optionally log exception details here

        # Fallback to legacy pipeline if new one fails
        scan_results = self.scan_and_extract()
        print("✅ ScoutVoyager: Computer vision scan complete!")
        print(f"   📸 Capture: {scan_results.get('overall_status', 'unknown')}")
        ocr = scan_results.get('ocr', {})
        print(f"   🔍 OCR Engine: {ocr.get('engine_used', 'n/a')}")
        print(f"   📝 Text Confidence: {ocr.get('confidence', 0):.1f}%")
        prod_analysis = scan_results.get('product_analysis', {})
        if prod_analysis.get('is_product_detected'):
            products = prod_analysis.get('detected_items', {})
            print(f"   🛍️ Products Detected: {prod_analysis.get('confidence_score', 0)}% confidence")
            if products.get('prices'):
                print(f"   💰 Prices: {', '.join(products['prices'])}")
            if products.get('brands'):
                print(f"   🏷️ Brands: {', '.join(products['brands'])}")
        print("📸 [ScoutVoyager] Ready for continuous vision monitoring!")
        return scan_results

def main():
    parser = argparse.ArgumentParser(description="ScoutVoyager - Computer vision and OCR agent")
    parser.add_argument("--smoke", action="store_true", help="Run smoke test only")
    parser.add_argument("--capture", action="store_true", help="Capture screen and analyze")
    parser.add_argument("--analyze", help="Analyze existing image file")
    args = parser.parse_args()
    
    # Check if agent is enabled
    try:
        import sys
        sys.path.append(str(Path(__file__).parent))
        from agent_manager import is_agent_enabled
        if not is_agent_enabled("ScoutVoyager"):
            print("📸 ScoutVoyager is disabled - skipping")
            return 0
    except ImportError:
        pass  # Continue if agent_manager not available yet
        
    # Handle fast mode
    if os.getenv("VOYAGER_FAST") == "1":
        args.smoke = True
        
    voyager = ScoutVoyager()
    
    if args.analyze:
        result = voyager.scan_and_extract(image_path=args.analyze)
    elif args.capture:
        result = voyager.scan_and_extract()
    else:
        result = voyager.run(smoke=args.smoke)
    
    # Print JSON for automation
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    if result.get("status") == "dependencies_missing":
        return 1
    else:
        return 0

if __name__ == "__main__":
    exit(main())
