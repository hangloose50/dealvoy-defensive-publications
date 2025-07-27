#!/usr/bin/env python3
"""
UPCVerifierAI Agent
UPC code verification and validation specialist agent
Protected by USPTO #63/850,603
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import re
import math

class UPCVerifierAI:
    """AI agent for UPC code verification, validation, and generation"""
    
    def __init__(self):
        self.agent_name = "UPCVerifierAI"
        self.version = "1.0.0"
        self.status = "active"
        self.supported_formats = ["UPC-A", "UPC-E", "EAN-13", "EAN-8", "ISBN-10", "ISBN-13"]
        self.verification_methods = ["checksum", "format", "database_lookup", "pattern_analysis"]
        
    def verify_upc_codes(self, verification_config: Dict[str, Any]) -> Dict[str, Any]:
        """Verify UPC codes for accuracy and validity"""
        try:
            upc_codes = verification_config.get("upc_codes", [])
            verification_methods = verification_config.get("methods", ["checksum", "format"])
            include_suggestions = verification_config.get("include_suggestions", True)
            batch_processing = verification_config.get("batch_processing", True)
            
            verification_id = f"upc_verify_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Validate input
            if not upc_codes:
                return {"error": "No UPC codes provided for verification"}
            
            # Process UPC codes
            verification_results = []
            
            if batch_processing:
                verification_results = self._batch_verify_upcs(upc_codes, verification_methods)
            else:
                for upc_code in upc_codes:
                    result = self._verify_single_upc(upc_code, verification_methods)
                    verification_results.append(result)
            
            # Generate analysis summary
            analysis_summary = self._analyze_verification_results(verification_results)
            
            # Generate suggestions if requested
            suggestions = []
            if include_suggestions:
                suggestions = self._generate_upc_suggestions(verification_results)
            
            # Detect patterns and anomalies
            pattern_analysis = self._analyze_upc_patterns(verification_results)
            
            result = {
                "verification_id": verification_id,
                "total_codes_processed": len(upc_codes),
                "verification_methods": verification_methods,
                "verification_results": verification_results,
                "analysis_summary": analysis_summary,
                "suggestions": suggestions,
                "pattern_analysis": pattern_analysis,
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"UPCVerifierAI verified {len(upc_codes)} UPC codes with {analysis_summary['valid_count']} valid")
            return result
            
        except Exception as e:
            logging.error(f"UPC verification failed: {e}")
            return {"error": str(e)}
    
    def generate_upc_codes(self, generation_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate valid UPC codes for products"""
        try:
            count = generation_config.get("count", 1)
            upc_format = generation_config.get("format", "UPC-A")
            manufacturer_code = generation_config.get("manufacturer_code", None)
            product_category = generation_config.get("product_category", "general")
            ensure_uniqueness = generation_config.get("ensure_uniqueness", True)
            
            generation_id = f"upc_gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Validate format
            if upc_format not in self.supported_formats:
                return {"error": f"Unsupported UPC format: {upc_format}"}
            
            # Generate UPC codes
            generated_codes = []
            used_codes = set()
            
            for i in range(count):
                attempts = 0
                while attempts < 10:  # Prevent infinite loops
                    upc_code = self._generate_single_upc(upc_format, manufacturer_code, product_category)
                    
                    if not ensure_uniqueness or upc_code not in used_codes:
                        generated_codes.append({
                            "upc_code": upc_code,
                            "format": upc_format,
                            "manufacturer_code": self._extract_manufacturer_code(upc_code, upc_format),
                            "product_code": self._extract_product_code(upc_code, upc_format),
                            "check_digit": self._extract_check_digit(upc_code, upc_format),
                            "validation_status": "valid"
                        })
                        used_codes.add(upc_code)
                        break
                    
                    attempts += 1
                
                if attempts >= 10:
                    logging.warning(f"Could not generate unique UPC code after 10 attempts")
            
            # Generate batch information
            batch_info = self._generate_batch_info(generated_codes, generation_config)
            
            # Validate all generated codes
            validation_results = self._validate_generated_codes(generated_codes)
            
            result = {
                "generation_id": generation_id,
                "requested_count": count,
                "generated_count": len(generated_codes),
                "upc_format": upc_format,
                "generated_codes": generated_codes,
                "batch_info": batch_info,
                "validation_results": validation_results,
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"UPCVerifierAI generated {len(generated_codes)} {upc_format} codes")
            return result
            
        except Exception as e:
            logging.error(f"UPC generation failed: {e}")
            return {"error": str(e)}
    
    def lookup_product_info(self, lookup_config: Dict[str, Any]) -> Dict[str, Any]:
        """Lookup product information using UPC codes"""
        try:
            upc_codes = lookup_config.get("upc_codes", [])
            lookup_sources = lookup_config.get("sources", ["internal_db", "external_apis"])
            include_images = lookup_config.get("include_images", False)
            detailed_info = lookup_config.get("detailed_info", True)
            
            lookup_id = f"upc_lookup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Process lookups
            lookup_results = []
            
            for upc_code in upc_codes:
                # First verify the UPC is valid
                verification = self._verify_single_upc(upc_code, ["checksum", "format"])
                
                if verification["is_valid"]:
                    # Perform product lookup
                    product_info = self._lookup_product_by_upc(upc_code, lookup_sources, include_images, detailed_info)
                    lookup_results.append({
                        "upc_code": upc_code,
                        "verification": verification,
                        "product_info": product_info,
                        "lookup_status": "success" if product_info else "not_found"
                    })
                else:
                    lookup_results.append({
                        "upc_code": upc_code,
                        "verification": verification,
                        "product_info": None,
                        "lookup_status": "invalid_upc"
                    })
            
            # Generate lookup statistics
            lookup_stats = self._generate_lookup_statistics(lookup_results)
            
            result = {
                "lookup_id": lookup_id,
                "total_lookups": len(upc_codes),
                "lookup_sources": lookup_sources,
                "lookup_results": lookup_results,
                "lookup_statistics": lookup_stats,
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"UPCVerifierAI looked up {len(upc_codes)} UPC codes with {lookup_stats['found_count']} found")
            return result
            
        except Exception as e:
            logging.error(f"UPC lookup failed: {e}")
            return {"error": str(e)}
    
    def analyze_upc_database(self, analysis_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze UPC database for patterns and anomalies"""
        try:
            database_source = analysis_config.get("database_source", "internal")
            analysis_types = analysis_config.get("analysis_types", ["duplicates", "patterns", "anomalies"])
            manufacturer_analysis = analysis_config.get("manufacturer_analysis", True)
            category_breakdown = analysis_config.get("category_breakdown", True)
            
            analysis_id = f"upc_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Simulate database analysis (in real implementation, would connect to actual database)
            sample_data = self._generate_sample_upc_data()
            
            analysis_results = {}
            
            if "duplicates" in analysis_types:
                analysis_results["duplicate_analysis"] = self._analyze_duplicate_upcs(sample_data)
            
            if "patterns" in analysis_types:
                analysis_results["pattern_analysis"] = self._analyze_upc_patterns_database(sample_data)
            
            if "anomalies" in analysis_types:
                analysis_results["anomaly_analysis"] = self._analyze_upc_anomalies(sample_data)
            
            if manufacturer_analysis:
                analysis_results["manufacturer_analysis"] = self._analyze_manufacturer_codes(sample_data)
            
            if category_breakdown:
                analysis_results["category_breakdown"] = self._analyze_product_categories(sample_data)
            
            # Generate recommendations
            recommendations = self._generate_database_recommendations(analysis_results)
            
            # Calculate database health score
            health_score = self._calculate_database_health_score(analysis_results)
            
            result = {
                "analysis_id": analysis_id,
                "database_source": database_source,
                "analysis_types": analysis_types,
                "sample_size": len(sample_data),
                "analysis_results": analysis_results,
                "recommendations": recommendations,
                "database_health_score": health_score,
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"UPCVerifierAI analyzed UPC database with health score {health_score}")
            return result
            
        except Exception as e:
            logging.error(f"UPC database analysis failed: {e}")
            return {"error": str(e)}
    
    def _batch_verify_upcs(self, upc_codes: List[str], methods: List[str]) -> List[Dict[str, Any]]:
        """Batch verify multiple UPC codes efficiently"""
        results = []
        
        # Group by format for efficient processing
        format_groups = {}
        for upc_code in upc_codes:
            upc_format = self._detect_upc_format(upc_code)
            if upc_format not in format_groups:
                format_groups[upc_format] = []
            format_groups[upc_format].append(upc_code)
        
        # Process each format group
        for upc_format, codes in format_groups.items():
            for code in codes:
                result = self._verify_single_upc(code, methods)
                results.append(result)
        
        return results
    
    def _verify_single_upc(self, upc_code: str, methods: List[str]) -> Dict[str, Any]:
        """Verify a single UPC code"""
        verification_result = {
            "upc_code": upc_code,
            "original_input": upc_code,
            "cleaned_code": self._clean_upc_code(upc_code),
            "detected_format": self._detect_upc_format(upc_code),
            "is_valid": False,
            "validation_details": {},
            "errors": []
        }
        
        cleaned_code = verification_result["cleaned_code"]
        detected_format = verification_result["detected_format"]
        
        # Perform requested verification methods
        all_checks_passed = True
        
        if "format" in methods:
            format_check = self._verify_format(cleaned_code, detected_format)
            verification_result["validation_details"]["format_check"] = format_check
            if not format_check["valid"]:
                all_checks_passed = False
                verification_result["errors"].extend(format_check.get("errors", []))
        
        if "checksum" in methods:
            checksum_check = self._verify_checksum(cleaned_code, detected_format)
            verification_result["validation_details"]["checksum_check"] = checksum_check
            if not checksum_check["valid"]:
                all_checks_passed = False
                verification_result["errors"].extend(checksum_check.get("errors", []))
        
        if "database_lookup" in methods:
            db_check = self._verify_database_lookup(cleaned_code)
            verification_result["validation_details"]["database_check"] = db_check
            # Database lookup failure doesn't invalidate UPC, just provides additional info
        
        if "pattern_analysis" in methods:
            pattern_check = self._verify_pattern_analysis(cleaned_code, detected_format)
            verification_result["validation_details"]["pattern_check"] = pattern_check
        
        verification_result["is_valid"] = all_checks_passed
        
        return verification_result
    
    def _clean_upc_code(self, upc_code: str) -> str:
        """Clean and normalize UPC code"""
        # Remove non-digit characters except hyphens
        cleaned = re.sub(r'[^0-9\-]', '', str(upc_code))
        
        # Remove hyphens
        cleaned = cleaned.replace('-', '')
        
        return cleaned
    
    def _detect_upc_format(self, upc_code: str) -> str:
        """Detect UPC format based on length and pattern"""
        cleaned = self._clean_upc_code(upc_code)
        length = len(cleaned)
        
        if length == 12:
            return "UPC-A"
        elif length == 8:
            return "UPC-E"
        elif length == 13:
            return "EAN-13"
        elif length == 8 and not cleaned.startswith('0'):
            return "EAN-8"
        elif length == 10:
            return "ISBN-10"
        elif length == 13 and (cleaned.startswith('978') or cleaned.startswith('979')):
            return "ISBN-13"
        else:
            return "unknown"
    
    def _verify_format(self, cleaned_code: str, detected_format: str) -> Dict[str, Any]:
        """Verify UPC format compliance"""
        errors = []
        
        if detected_format == "unknown":
            errors.append(f"Unknown format for code length {len(cleaned_code)}")
            return {"valid": False, "errors": errors, "format": detected_format}
        
        # Check if all characters are digits
        if not cleaned_code.isdigit():
            errors.append("UPC code contains non-digit characters")
        
        # Format-specific validations
        if detected_format == "UPC-A" and len(cleaned_code) != 12:
            errors.append(f"UPC-A must be 12 digits, got {len(cleaned_code)}")
        elif detected_format == "UPC-E" and len(cleaned_code) != 8:
            errors.append(f"UPC-E must be 8 digits, got {len(cleaned_code)}")
        elif detected_format == "EAN-13" and len(cleaned_code) != 13:
            errors.append(f"EAN-13 must be 13 digits, got {len(cleaned_code)}")
        elif detected_format == "EAN-8" and len(cleaned_code) != 8:
            errors.append(f"EAN-8 must be 8 digits, got {len(cleaned_code)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "format": detected_format,
            "length": len(cleaned_code)
        }
    
    def _verify_checksum(self, cleaned_code: str, detected_format: str) -> Dict[str, Any]:
        """Verify UPC checksum digit"""
        if not cleaned_code.isdigit():
            return {"valid": False, "errors": ["Non-digit characters in UPC code"]}
        
        if detected_format in ["UPC-A", "EAN-13"]:
            return self._verify_upc_a_checksum(cleaned_code)
        elif detected_format == "UPC-E":
            return self._verify_upc_e_checksum(cleaned_code)
        elif detected_format == "EAN-8":
            return self._verify_ean_8_checksum(cleaned_code)
        elif detected_format in ["ISBN-10", "ISBN-13"]:
            return self._verify_isbn_checksum(cleaned_code, detected_format)
        else:
            return {"valid": False, "errors": [f"Checksum verification not implemented for {detected_format}"]}
    
    def _verify_upc_a_checksum(self, code: str) -> Dict[str, Any]:
        """Verify UPC-A checksum using the standard algorithm"""
        if len(code) != 12:
            return {"valid": False, "errors": ["UPC-A must be 12 digits for checksum verification"]}
        
        # Extract digits
        digits = [int(d) for d in code]
        
        # Calculate checksum
        odd_sum = sum(digits[i] for i in range(0, 11, 2))  # 1st, 3rd, 5th, etc.
        even_sum = sum(digits[i] for i in range(1, 11, 2))  # 2nd, 4th, 6th, etc.
        
        total = (odd_sum * 3) + even_sum
        calculated_check_digit = (10 - (total % 10)) % 10
        
        actual_check_digit = digits[11]
        
        return {
            "valid": calculated_check_digit == actual_check_digit,
            "calculated_check_digit": calculated_check_digit,
            "actual_check_digit": actual_check_digit,
            "errors": [] if calculated_check_digit == actual_check_digit else ["Checksum verification failed"]
        }
    
    def _verify_upc_e_checksum(self, code: str) -> Dict[str, Any]:
        """Verify UPC-E checksum (simplified implementation)"""
        if len(code) != 8:
            return {"valid": False, "errors": ["UPC-E must be 8 digits for checksum verification"]}
        
        # For UPC-E, we would need to expand to UPC-A first, then verify
        # This is a simplified implementation
        digits = [int(d) for d in code]
        
        # Simplified checksum calculation for demonstration
        total = sum(digits[i] * (3 if i % 2 == 0 else 1) for i in range(7))
        calculated_check_digit = (10 - (total % 10)) % 10
        actual_check_digit = digits[7]
        
        return {
            "valid": calculated_check_digit == actual_check_digit,
            "calculated_check_digit": calculated_check_digit,
            "actual_check_digit": actual_check_digit,
            "errors": [] if calculated_check_digit == actual_check_digit else ["UPC-E checksum verification failed"]
        }
    
    def _verify_ean_8_checksum(self, code: str) -> Dict[str, Any]:
        """Verify EAN-8 checksum"""
        if len(code) != 8:
            return {"valid": False, "errors": ["EAN-8 must be 8 digits for checksum verification"]}
        
        digits = [int(d) for d in code]
        
        # EAN-8 checksum calculation
        odd_sum = sum(digits[i] for i in range(0, 7, 2))  # 1st, 3rd, 5th, 7th
        even_sum = sum(digits[i] for i in range(1, 7, 2))  # 2nd, 4th, 6th
        
        total = odd_sum + (even_sum * 3)
        calculated_check_digit = (10 - (total % 10)) % 10
        actual_check_digit = digits[7]
        
        return {
            "valid": calculated_check_digit == actual_check_digit,
            "calculated_check_digit": calculated_check_digit,
            "actual_check_digit": actual_check_digit,
            "errors": [] if calculated_check_digit == actual_check_digit else ["EAN-8 checksum verification failed"]
        }
    
    def _verify_isbn_checksum(self, code: str, format_type: str) -> Dict[str, Any]:
        """Verify ISBN checksum"""
        if format_type == "ISBN-10":
            return self._verify_isbn_10_checksum(code)
        elif format_type == "ISBN-13":
            return self._verify_isbn_13_checksum(code)
        else:
            return {"valid": False, "errors": ["Unknown ISBN format"]}
    
    def _verify_isbn_10_checksum(self, code: str) -> Dict[str, Any]:
        """Verify ISBN-10 checksum"""
        if len(code) != 10:
            return {"valid": False, "errors": ["ISBN-10 must be 10 characters"]}
        
        # ISBN-10 can have 'X' as check digit
        digits = []
        for i, char in enumerate(code):
            if i == 9 and char.upper() == 'X':
                digits.append(10)
            elif char.isdigit():
                digits.append(int(char))
            else:
                return {"valid": False, "errors": ["Invalid character in ISBN-10"]}
        
        # Calculate checksum
        total = sum(digits[i] * (10 - i) for i in range(9))
        calculated_check = (11 - (total % 11)) % 11
        
        return {
            "valid": calculated_check == digits[9],
            "calculated_check_digit": calculated_check if calculated_check != 10 else 'X',
            "actual_check_digit": digits[9] if digits[9] != 10 else 'X',
            "errors": [] if calculated_check == digits[9] else ["ISBN-10 checksum verification failed"]
        }
    
    def _verify_isbn_13_checksum(self, code: str) -> Dict[str, Any]:
        """Verify ISBN-13 checksum (same as EAN-13)"""
        return self._verify_upc_a_checksum(code)  # ISBN-13 uses same algorithm as EAN-13/UPC-A
    
    def _verify_database_lookup(self, cleaned_code: str) -> Dict[str, Any]:
        """Verify UPC against database (simulated)"""
        # Simulate database lookup
        # In real implementation, this would query actual product databases
        
        known_upcs = {
            "123456789012": {"product": "Sample Product A", "manufacturer": "Company A", "category": "Electronics"},
            "987654321098": {"product": "Sample Product B", "manufacturer": "Company B", "category": "Books"},
            "456789012345": {"product": "Sample Product C", "manufacturer": "Company C", "category": "Clothing"}
        }
        
        if cleaned_code in known_upcs:
            return {
                "found_in_database": True,
                "product_info": known_upcs[cleaned_code],
                "database_confidence": "high"
            }
        else:
            return {
                "found_in_database": False,
                "product_info": None,
                "database_confidence": "not_applicable"
            }
    
    def _verify_pattern_analysis(self, cleaned_code: str, detected_format: str) -> Dict[str, Any]:
        """Analyze UPC patterns for anomalies"""
        analysis = {
            "pattern_valid": True,
            "anomalies": [],
            "pattern_type": "standard"
        }
        
        if detected_format == "UPC-A":
            # Check for common pattern anomalies
            if cleaned_code.startswith("000000"):
                analysis["anomalies"].append("UPC starts with six zeros (unusual)")
            
            if cleaned_code.endswith("000000"):
                analysis["anomalies"].append("UPC ends with six zeros (unusual)")
            
            # Check for repeating patterns
            if len(set(cleaned_code)) <= 2:
                analysis["anomalies"].append("UPC contains mostly repeating digits")
            
            # Check for sequential patterns
            if self._is_sequential_pattern(cleaned_code):
                analysis["anomalies"].append("UPC contains sequential digit pattern")
        
        analysis["pattern_valid"] = len(analysis["anomalies"]) == 0
        
        return analysis
    
    def _is_sequential_pattern(self, code: str) -> bool:
        """Check if code contains sequential digit patterns"""
        # Check for ascending sequences
        for i in range(len(code) - 4):
            substring = code[i:i+5]
            if all(int(substring[j]) == int(substring[0]) + j for j in range(5)):
                return True
        
        # Check for descending sequences
        for i in range(len(code) - 4):
            substring = code[i:i+5]
            if all(int(substring[j]) == int(substring[0]) - j for j in range(5)):
                return True
        
        return False
    
    def _generate_single_upc(self, upc_format: str, manufacturer_code: Optional[str], product_category: str) -> str:
        """Generate a single valid UPC code"""
        if upc_format == "UPC-A":
            return self._generate_upc_a(manufacturer_code, product_category)
        elif upc_format == "UPC-E":
            return self._generate_upc_e(manufacturer_code, product_category)
        elif upc_format == "EAN-13":
            return self._generate_ean_13(manufacturer_code, product_category)
        elif upc_format == "EAN-8":
            return self._generate_ean_8(product_category)
        else:
            return self._generate_upc_a(manufacturer_code, product_category)  # Default to UPC-A
    
    def _generate_upc_a(self, manufacturer_code: Optional[str], product_category: str) -> str:
        """Generate a valid UPC-A code"""
        import random
        
        # Use provided manufacturer code or generate one
        if manufacturer_code and len(manufacturer_code) >= 6:
            manuf_code = manufacturer_code[:6]
        else:
            manuf_code = f"{random.randint(100000, 999999):06d}"
        
        # Generate product code based on category
        category_prefixes = {
            "electronics": "001",
            "books": "002",
            "clothing": "003",
            "food": "004",
            "toys": "005",
            "general": "000"
        }
        
        category_prefix = category_prefixes.get(product_category, "000")
        product_code = f"{category_prefix}{random.randint(100, 999):03d}"
        
        # Combine manufacturer and product codes (11 digits)
        base_code = manuf_code + product_code[:5]  # Ensure total is 11 digits
        
        # Calculate and append check digit
        check_digit = self._calculate_upc_a_check_digit(base_code)
        
        return base_code + str(check_digit)
    
    def _calculate_upc_a_check_digit(self, code: str) -> int:
        """Calculate UPC-A check digit"""
        if len(code) != 11:
            raise ValueError("Code must be 11 digits for UPC-A check digit calculation")
        
        digits = [int(d) for d in code]
        
        odd_sum = sum(digits[i] for i in range(0, 11, 2))
        even_sum = sum(digits[i] for i in range(1, 11, 2))
        
        total = (odd_sum * 3) + even_sum
        check_digit = (10 - (total % 10)) % 10
        
        return check_digit
    
    def _generate_upc_e(self, manufacturer_code: Optional[str], product_category: str) -> str:
        """Generate a valid UPC-E code (simplified)"""
        import random
        
        # Generate 7 random digits
        base_digits = [random.randint(0, 9) for _ in range(7)]
        
        # Calculate check digit (simplified for UPC-E)
        total = sum(base_digits[i] * (3 if i % 2 == 0 else 1) for i in range(7))
        check_digit = (10 - (total % 10)) % 10
        
        return ''.join(str(d) for d in base_digits) + str(check_digit)
    
    def _generate_ean_13(self, manufacturer_code: Optional[str], product_category: str) -> str:
        """Generate a valid EAN-13 code"""
        import random
        
        # Start with country code (e.g., 123 for test)
        country_code = "123"
        
        # Use manufacturer code or generate
        if manufacturer_code and len(manufacturer_code) >= 4:
            manuf_code = manufacturer_code[:4]
        else:
            manuf_code = f"{random.randint(1000, 9999):04d}"
        
        # Generate product code
        product_code = f"{random.randint(10000, 99999):05d}"
        
        # Combine (12 digits)
        base_code = country_code + manuf_code + product_code
        
        # Calculate check digit using UPC-A algorithm
        check_digit = self._calculate_upc_a_check_digit(base_code)
        
        return base_code + str(check_digit)
    
    def _generate_ean_8(self, product_category: str) -> str:
        """Generate a valid EAN-8 code"""
        import random
        
        # Generate 7 random digits
        base_digits = [random.randint(0, 9) for _ in range(7)]
        
        # Calculate EAN-8 check digit
        odd_sum = sum(base_digits[i] for i in range(0, 7, 2))
        even_sum = sum(base_digits[i] for i in range(1, 7, 2))
        
        total = odd_sum + (even_sum * 3)
        check_digit = (10 - (total % 10)) % 10
        
        return ''.join(str(d) for d in base_digits) + str(check_digit)
    
    def _extract_manufacturer_code(self, upc_code: str, upc_format: str) -> str:
        """Extract manufacturer code from UPC"""
        if upc_format == "UPC-A":
            return upc_code[:6]
        elif upc_format == "EAN-13":
            return upc_code[3:7]  # After country code
        else:
            return upc_code[:4]  # Generic extraction
    
    def _extract_product_code(self, upc_code: str, upc_format: str) -> str:
        """Extract product code from UPC"""
        if upc_format == "UPC-A":
            return upc_code[6:11]
        elif upc_format == "EAN-13":
            return upc_code[7:12]
        else:
            return upc_code[4:-1]  # Generic extraction (excluding check digit)
    
    def _extract_check_digit(self, upc_code: str, upc_format: str) -> str:
        """Extract check digit from UPC"""
        return upc_code[-1]
    
    def _analyze_verification_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze verification results and generate summary"""
        total_codes = len(results)
        valid_codes = len([r for r in results if r["is_valid"]])
        invalid_codes = total_codes - valid_codes
        
        # Analyze error types
        error_types = {}
        for result in results:
            for error in result.get("errors", []):
                error_types[error] = error_types.get(error, 0) + 1
        
        # Analyze formats
        format_distribution = {}
        for result in results:
            format_type = result.get("detected_format", "unknown")
            format_distribution[format_type] = format_distribution.get(format_type, 0) + 1
        
        return {
            "total_codes": total_codes,
            "valid_count": valid_codes,
            "invalid_count": invalid_codes,
            "validity_rate": round((valid_codes / total_codes) * 100, 2) if total_codes > 0 else 0,
            "error_types": error_types,
            "format_distribution": format_distribution,
            "most_common_error": max(error_types, key=error_types.get) if error_types else None
        }
    
    def _generate_upc_suggestions(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate suggestions for fixing invalid UPC codes"""
        suggestions = []
        
        for result in results:
            if not result["is_valid"]:
                upc_code = result["upc_code"]
                errors = result.get("errors", [])
                
                suggestion = {
                    "original_upc": upc_code,
                    "errors": errors,
                    "suggestions": []
                }
                
                # Generate specific suggestions based on errors
                for error in errors:
                    if "checksum" in error.lower():
                        # Suggest corrected check digit
                        corrected_upc = self._suggest_corrected_checksum(upc_code, result["detected_format"])
                        if corrected_upc:
                            suggestion["suggestions"].append({
                                "type": "checksum_correction",
                                "corrected_upc": corrected_upc,
                                "description": "Corrected check digit based on UPC algorithm"
                            })
                    
                    if "length" in error.lower() or "format" in error.lower():
                        # Suggest padding or truncation
                        formatted_upc = self._suggest_format_correction(upc_code)
                        if formatted_upc:
                            suggestion["suggestions"].append({
                                "type": "format_correction",
                                "corrected_upc": formatted_upc,
                                "description": "Adjusted length/format to standard UPC format"
                            })
                
                if suggestion["suggestions"]:
                    suggestions.append(suggestion)
        
        return suggestions
    
    def _suggest_corrected_checksum(self, upc_code: str, detected_format: str) -> Optional[str]:
        """Suggest UPC with corrected check digit"""
        cleaned = self._clean_upc_code(upc_code)
        
        if detected_format == "UPC-A" and len(cleaned) == 12:
            base_code = cleaned[:11]
            corrected_check_digit = self._calculate_upc_a_check_digit(base_code)
            return base_code + str(corrected_check_digit)
        
        # Add similar logic for other formats
        return None
    
    def _suggest_format_correction(self, upc_code: str) -> Optional[str]:
        """Suggest format correction for UPC"""
        cleaned = self._clean_upc_code(upc_code)
        
        # If too short, pad with zeros
        if len(cleaned) < 12:
            padded = cleaned.zfill(12)
            # Recalculate check digit
            base_code = padded[:11]
            check_digit = self._calculate_upc_a_check_digit(base_code)
            return base_code + str(check_digit)
        
        # If too long, truncate (be careful with this)
        if len(cleaned) > 12:
            truncated = cleaned[:12]
            # Recalculate check digit
            base_code = truncated[:11]
            check_digit = self._calculate_upc_a_check_digit(base_code)
            return base_code + str(check_digit)
        
        return None
    
    def _analyze_upc_patterns(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in UPC verification results"""
        patterns = {
            "manufacturer_codes": {},
            "common_prefixes": {},
            "length_distribution": {},
            "anomaly_patterns": []
        }
        
        for result in results:
            upc_code = result.get("cleaned_code", "")
            detected_format = result.get("detected_format", "unknown")
            
            # Analyze manufacturer codes (first 6 digits for UPC-A)
            if detected_format == "UPC-A" and len(upc_code) >= 6:
                manuf_code = upc_code[:6]
                patterns["manufacturer_codes"][manuf_code] = patterns["manufacturer_codes"].get(manuf_code, 0) + 1
            
            # Analyze common prefixes
            if len(upc_code) >= 3:
                prefix = upc_code[:3]
                patterns["common_prefixes"][prefix] = patterns["common_prefixes"].get(prefix, 0) + 1
            
            # Length distribution
            length = len(upc_code)
            patterns["length_distribution"][length] = patterns["length_distribution"].get(length, 0) + 1
            
            # Check for anomaly patterns
            if result.get("validation_details", {}).get("pattern_check", {}).get("anomalies"):
                patterns["anomaly_patterns"].extend(
                    result["validation_details"]["pattern_check"]["anomalies"]
                )
        
        return patterns
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        input_data = input_data or {}
        
        operation = input_data.get("operation", "status")
        
        if operation == "verify" and "verification_config" in input_data:
            return self.verify_upc_codes(input_data["verification_config"])
        elif operation == "generate" and "generation_config" in input_data:
            return self.generate_upc_codes(input_data["generation_config"])
        elif operation == "lookup" and "lookup_config" in input_data:
            return self.lookup_product_info(input_data["lookup_config"])
        elif operation == "analyze_database" and "analysis_config" in input_data:
            return self.analyze_upc_database(input_data["analysis_config"])
        
        return {
            "status": "ready",
            "agent": self.agent_name,
            "capabilities": ["upc_verification", "upc_generation", "product_lookup", "database_analysis"],
            "supported_formats": self.supported_formats,
            "verification_methods": self.verification_methods
        }

if __name__ == "__main__":
    agent = UPCVerifierAI()
    print(json.dumps(agent.run(), indent=2))
