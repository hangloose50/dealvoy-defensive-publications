#!/usr/bin/env python3
"""
🔭 ScoutVision OCR - Computer Vision + OCR Pipeline
Captures frames, runs Tesseract OCR, extracts product text with bounding boxes
"""

import cv2
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

class ScoutOCR:
    def __init__(self, project_path="."):
        self.project_path = Path(project_path)
        self.vision_dir = self.project_path / "app" / "vision"
        self.vision_dir.mkdir(parents=True, exist_ok=True)
        
        # OCR Results directory
        self.ocr_results_dir = self.vision_dir / "ocr_results"
        self.ocr_results_dir.mkdir(parents=True, exist_ok=True)
        
    def check_dependencies(self):
        """Check if required vision libraries are available"""
        status = {
            "tesseract": TESSERACT_AVAILABLE,
            "opencv": OPENCV_AVAILABLE,
            "ready": TESSERACT_AVAILABLE and OPENCV_AVAILABLE
        }
        
        if not status["ready"]:
            missing = []
            if not TESSERACT_AVAILABLE:
                missing.append("pytesseract (pip install pytesseract)")
            if not OPENCV_AVAILABLE:
                missing.append("opencv-python (pip install opencv-python)")
            
            status["missing_dependencies"] = missing
            
        return status
        
    def capture_frame(self, camera_index=0, fallback_image="./sample.jpg"):
        """Capture frame from camera or use fallback image"""
        frame = None
        source = "fallback"
        
        if OPENCV_AVAILABLE:
            try:
                # Try to capture from camera
                cap = cv2.VideoCapture(camera_index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        source = f"camera_{camera_index}"
                        # Save captured frame for debugging
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        cv2.imwrite(str(self.vision_dir / f"captured_{timestamp}.jpg"), frame)
                    cap.release()
            except Exception as e:
                print(f"📷 Camera capture failed: {e}")
                
        # Fallback to sample image
        if frame is None:
            fallback_path = Path(fallback_image)
            if fallback_path.exists():
                if OPENCV_AVAILABLE:
                    frame = cv2.imread(str(fallback_path))
                    source = str(fallback_path)
            else:
                # Create a simple test image
                if OPENCV_AVAILABLE:
                    frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
                    cv2.putText(frame, "SAMPLE PRODUCT", (50, 240), 
                              cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
                    cv2.putText(frame, "UPC: 123456789012", (50, 300), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    cv2.putText(frame, "$19.99", (50, 350), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
                    source = "generated_sample"
                    
        return frame, source
        
    def extract_text_with_boxes(self, image) -> Dict:
        """Extract text with bounding boxes using Tesseract OCR"""
        if not TESSERACT_AVAILABLE or not OPENCV_AVAILABLE:
            return {
                "error": "OCR dependencies not available",
                "text_blocks": [],
                "raw_text": "",
                "confidence": 0
            }
            
        try:
            # Get detailed OCR data with bounding boxes
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            text_blocks = []
            raw_text_parts = []
            
            for i in range(len(ocr_data['text'])):
                text = ocr_data['text'][i].strip()
                if text and int(ocr_data['conf'][i]) > 30:  # Confidence threshold
                    x = ocr_data['left'][i]
                    y = ocr_data['top'][i]
                    w = ocr_data['width'][i]
                    h = ocr_data['height'][i]
                    conf = int(ocr_data['conf'][i])
                    
                    text_blocks.append({
                        "text": text,
                        "bbox": {"x": x, "y": y, "width": w, "height": h},
                        "confidence": conf,
                        "type": self._classify_text(text)
                    })
                    raw_text_parts.append(text)
            
            # Calculate overall confidence
            confidences = [block["confidence"] for block in text_blocks]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                "text_blocks": text_blocks,
                "raw_text": " ".join(raw_text_parts),
                "confidence": round(avg_confidence, 2),
                "total_blocks": len(text_blocks)
            }
            
        except Exception as e:
            return {
                "error": f"OCR extraction failed: {str(e)}",
                "text_blocks": [],
                "raw_text": "",
                "confidence": 0
            }
    
    def _classify_text(self, text: str) -> str:
        """Classify detected text into categories"""
        text_upper = text.upper()
        
        # UPC/Barcode patterns
        if re.match(r'^\d{12,14}$', text):
            return "upc"
        if re.match(r'^\d{13}$', text):
            return "ean"
        if re.match(r'^97[89]\d{10}$', text):
            return "isbn"
            
        # Price patterns
        if re.match(r'^\$?\d+\.?\d*$', text):
            return "price"
        if re.search(r'\$\d+', text):
            return "price"
            
        # Brand/Product patterns (common brands)
        brands = ["AMAZON", "APPLE", "SAMSUNG", "SONY", "LG", "HP", "DELL", "NIKE", "ADIDAS"]
        if any(brand in text_upper for brand in brands):
            return "brand"
            
        # Model numbers
        if re.match(r'^[A-Z0-9\-]+$', text) and len(text) > 3:
            return "model"
            
        return "text"
    
    def filter_product_text(self, ocr_result: Dict) -> Dict:
        """Filter and enhance OCR results for product matching"""
        if "text_blocks" not in ocr_result:
            return ocr_result
            
        filtered_blocks = {
            "upcs": [],
            "prices": [],
            "brands": [],
            "models": [],
            "product_text": []
        }
        
        for block in ocr_result["text_blocks"]:
            text_type = block["type"]
            text = block["text"]
            
            if text_type == "upc":
                filtered_blocks["upcs"].append({
                    "value": text,
                    "confidence": block["confidence"],
                    "bbox": block["bbox"]
                })
            elif text_type == "price":
                filtered_blocks["prices"].append({
                    "value": text,
                    "confidence": block["confidence"],
                    "bbox": block["bbox"]
                })
            elif text_type == "brand":
                filtered_blocks["brands"].append({
                    "value": text,
                    "confidence": block["confidence"],
                    "bbox": block["bbox"]
                })
            elif text_type == "model":
                filtered_blocks["models"].append({
                    "value": text,
                    "confidence": block["confidence"],
                    "bbox": block["bbox"]
                })
            else:
                filtered_blocks["product_text"].append({
                    "value": text,
                    "confidence": block["confidence"],
                    "bbox": block["bbox"]
                })
        
        # Add summary
        filtered_blocks["summary"] = {
            "primary_upc": filtered_blocks["upcs"][0]["value"] if filtered_blocks["upcs"] else None,
            "primary_price": filtered_blocks["prices"][0]["value"] if filtered_blocks["prices"] else None,
            "primary_brand": filtered_blocks["brands"][0]["value"] if filtered_blocks["brands"] else None,
            "confidence_score": ocr_result.get("confidence", 0)
        }
        
        return filtered_blocks
    
    def run_ocr_pipeline(self, camera_index=0, fallback_image="./sample.jpg", save_results=True):
        """Complete OCR pipeline: capture → extract → filter"""
        print("🔭 [ScoutOCR] Starting OCR pipeline...")
        
        # Check dependencies
        deps = self.check_dependencies()
        if not deps["ready"]:
            return {
                "status": "error",
                "message": "Missing dependencies",
                "missing": deps.get("missing_dependencies", [])
            }
        
        # Capture frame
        print("📷 Capturing frame...")
        frame, source = self.capture_frame(camera_index, fallback_image)
        
        if frame is None:
            return {
                "status": "error",
                "message": "Failed to capture or load image"
            }
        
        print(f"📷 Image source: {source}")
        
        # Extract text
        print("🔍 Running OCR extraction...")
        ocr_result = self.extract_text_with_boxes(frame)
        
        if "error" in ocr_result:
            return {
                "status": "error",
                "message": ocr_result["error"]
            }
        
        # Filter for product data
        print("🏷️ Filtering product information...")
        filtered_result = self.filter_product_text(ocr_result)
        
        # Compile results
        pipeline_result = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "raw_ocr": ocr_result,
            "filtered_data": filtered_result,
            "status": "success"
        }
        
        # Save results
        if save_results:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_file = self.ocr_results_dir / f"ocr_result_{timestamp}.json"
            with open(result_file, 'w') as f:
                json.dump(pipeline_result, f, indent=2)
            print(f"📄 Results saved: {result_file}")
        
        # Print summary
        summary = filtered_result.get("summary", {})
        print("\n🔭 OCR Pipeline Results:")
        print(f"   📊 Confidence: {ocr_result.get('confidence', 0)}%")
        print(f"   🏷️ UPC: {summary.get('primary_upc', 'None detected')}")
        print(f"   💰 Price: {summary.get('primary_price', 'None detected')}")
        print(f"   🏭 Brand: {summary.get('primary_brand', 'None detected')}")
        print(f"   📝 Text Blocks: {ocr_result.get('total_blocks', 0)}")
        
        return pipeline_result

def main():
    """Test the OCR pipeline"""
    scout = ScoutOCR()
    result = scout.run_ocr_pipeline()
    
    if result.get("status") == "success":
        print("\n✅ ScoutOCR pipeline test successful!")
    else:
        print(f"\n❌ ScoutOCR pipeline failed: {result.get('message')}")
        
    return 0 if result.get("status") == "success" else 1

if __name__ == "__main__":
    exit(main())
