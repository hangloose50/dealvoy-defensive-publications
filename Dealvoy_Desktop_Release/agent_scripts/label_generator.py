#!/usr/bin/env python3
"""
LabelGenerator Agent
Product label and tag generation specialist agent
Protected by USPTO #63/850,603
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List
import random
import base64

class LabelGenerator:
    """AI agent for generating product labels, tags, and identification elements"""
    
    def __init__(self):
        self.agent_name = "LabelGenerator"
        self.version = "1.0.0"
        self.status = "active"
        self.label_types = ["shipping", "product", "barcode", "price", "warning", "custom"]
        self.formats = ["pdf", "png", "svg", "html", "zpl", "epl"]
        
    def generate_product_labels(self, label_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate product labels based on configuration"""
        try:
            products = label_config.get("products", [])
            label_type = label_config.get("label_type", "product")
            format_type = label_config.get("format", "pdf")
            template = label_config.get("template", "standard")
            
            batch_id = f"labels_{label_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Validate label configuration
            validation_result = self._validate_label_config(label_config)
            if not validation_result["valid"]:
                return {"error": validation_result["errors"]}
            
            # Generate labels for each product
            generated_labels = []
            for product in products:
                label_data = self._generate_single_label(product, label_type, template)
                generated_labels.append(label_data)
            
            # Format labels based on output format
            formatted_output = self._format_label_output(generated_labels, format_type)
            
            # Calculate label statistics
            statistics = self._calculate_label_statistics(generated_labels, formatted_output)
            
            # Generate print instructions
            print_instructions = self._generate_print_instructions(label_config, statistics)
            
            result = {
                "batch_id": batch_id,
                "label_type": label_type,
                "format": format_type,
                "template": template,
                "total_labels": len(generated_labels),
                "label_data": generated_labels,
                "formatted_output": formatted_output,
                "statistics": statistics,
                "print_instructions": print_instructions,
                "generation_timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"LabelGenerator created {len(generated_labels)} {label_type} labels")
            return result
            
        except Exception as e:
            logging.error(f"Label generation failed: {e}")
            return {"error": str(e)}
    
    def generate_barcodes(self, barcode_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate barcodes for products"""
        try:
            products = barcode_config.get("products", [])
            barcode_type = barcode_config.get("barcode_type", "code128")
            include_text = barcode_config.get("include_text", True)
            size = barcode_config.get("size", "medium")
            
            batch_id = f"barcodes_{barcode_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            generated_barcodes = []
            for product in products:
                barcode_data = self._generate_barcode(product, barcode_type, include_text, size)
                generated_barcodes.append(barcode_data)
            
            # Package barcodes
            barcode_package = self._package_barcodes(generated_barcodes, barcode_config)
            
            result = {
                "batch_id": batch_id,
                "barcode_type": barcode_type,
                "total_barcodes": len(generated_barcodes),
                "barcodes": generated_barcodes,
                "package": barcode_package,
                "generation_timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Barcode generation failed: {e}")
            return {"error": str(e)}
    
    def generate_shipping_labels(self, shipping_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate shipping labels for orders"""
        try:
            orders = shipping_config.get("orders", [])
            carrier = shipping_config.get("carrier", "ups")
            label_size = shipping_config.get("label_size", "4x6")
            include_return = shipping_config.get("include_return_label", False)
            
            batch_id = f"shipping_{carrier}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            shipping_labels = []
            for order in orders:
                label_set = self._generate_shipping_label_set(order, carrier, label_size, include_return)
                shipping_labels.append(label_set)
            
            # Generate manifest
            manifest = self._generate_shipping_manifest(shipping_labels, carrier)
            
            # Calculate shipping costs
            cost_summary = self._calculate_shipping_costs(shipping_labels, carrier)
            
            result = {
                "batch_id": batch_id,
                "carrier": carrier,
                "label_size": label_size,
                "total_shipments": len(shipping_labels),
                "shipping_labels": shipping_labels,
                "manifest": manifest,
                "cost_summary": cost_summary,
                "tracking_info": self._generate_tracking_info(shipping_labels),
                "generation_timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Shipping label generation failed: {e}")
            return {"error": str(e)}
    
    def generate_custom_labels(self, custom_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate custom labels with user-defined templates"""
        try:
            template_config = custom_config.get("template", {})
            data_source = custom_config.get("data", [])
            customizations = custom_config.get("customizations", {})
            
            batch_id = f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Process template
            processed_template = self._process_custom_template(template_config, customizations)
            
            # Generate labels using template
            custom_labels = []
            for data_item in data_source:
                label = self._apply_template_to_data(processed_template, data_item)
                custom_labels.append(label)
            
            # Validate custom labels
            validation_results = self._validate_custom_labels(custom_labels, template_config)
            
            result = {
                "batch_id": batch_id,
                "template_used": template_config.get("name", "custom"),
                "total_labels": len(custom_labels),
                "custom_labels": custom_labels,
                "template_info": processed_template,
                "validation_results": validation_results,
                "generation_timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Custom label generation failed: {e}")
            return {"error": str(e)}
    
    def _validate_label_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate label configuration"""
        errors = []
        
        if not config.get("products"):
            errors.append("No products specified for label generation")
        
        label_type = config.get("label_type", "product")
        if label_type not in self.label_types:
            errors.append(f"Unsupported label type: {label_type}")
        
        format_type = config.get("format", "pdf")
        if format_type not in self.formats:
            errors.append(f"Unsupported format: {format_type}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _generate_single_label(self, product: Dict[str, Any], label_type: str, template: str) -> Dict[str, Any]:
        """Generate a single product label"""
        product_id = product.get("id", "UNKNOWN")
        product_name = product.get("name", "Product")
        price = product.get("price", 0.00)
        
        # Generate label content based on type
        if label_type == "product":
            label_content = self._generate_product_label_content(product, template)
        elif label_type == "price":
            label_content = self._generate_price_label_content(product, template)
        elif label_type == "shipping":
            label_content = self._generate_shipping_label_content(product, template)
        elif label_type == "barcode":
            label_content = self._generate_barcode_label_content(product, template)
        elif label_type == "warning":
            label_content = self._generate_warning_label_content(product, template)
        else:
            label_content = self._generate_generic_label_content(product, template)
        
        return {
            "product_id": product_id,
            "label_type": label_type,
            "content": label_content,
            "dimensions": self._get_label_dimensions(template),
            "print_settings": self._get_print_settings(label_type, template)
        }
    
    def _generate_product_label_content(self, product: Dict[str, Any], template: str) -> Dict[str, Any]:
        """Generate product label content"""
        return {
            "title": product.get("name", "Product Name"),
            "description": product.get("description", "")[:100] + "..." if len(product.get("description", "")) > 100 else product.get("description", ""),
            "price": f"${product.get('price', 0.00):.2f}",
            "sku": product.get("sku", product.get("id", "SKU-UNKNOWN")),
            "brand": product.get("brand", "Brand"),
            "category": product.get("category", "General"),
            "barcode": self._generate_product_barcode(product),
            "qr_code": self._generate_product_qr_code(product),
            "logo": {"type": "placeholder", "size": "small"}
        }
    
    def _generate_price_label_content(self, product: Dict[str, Any], template: str) -> Dict[str, Any]:
        """Generate price label content"""
        price = product.get("price", 0.00)
        original_price = product.get("original_price", price)
        discount = ((original_price - price) / original_price * 100) if original_price > price else 0
        
        return {
            "current_price": f"${price:.2f}",
            "original_price": f"${original_price:.2f}" if discount > 0 else None,
            "discount_percent": f"{discount:.0f}% OFF" if discount > 0 else None,
            "product_name": product.get("name", "Product")[:50],
            "sku": product.get("sku", product.get("id", "SKU")),
            "effective_date": datetime.now().strftime("%m/%d/%Y"),
            "barcode": self._generate_product_barcode(product)
        }
    
    def _generate_shipping_label_content(self, product: Dict[str, Any], template: str) -> Dict[str, Any]:
        """Generate shipping label content"""
        return {
            "sender": {
                "name": "Dealvoy Fulfillment",
                "address": "123 Business St",
                "city": "Business City",
                "state": "BC",
                "zip": "12345",
                "country": "USA"
            },
            "recipient": product.get("shipping_address", {
                "name": "Customer Name",
                "address": "456 Customer Ave",
                "city": "Customer City", 
                "state": "CC",
                "zip": "67890",
                "country": "USA"
            }),
            "tracking_number": f"DV{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}",
            "service_type": product.get("shipping_service", "Ground"),
            "weight": f"{product.get('weight', 1.0)} lbs",
            "declared_value": f"${product.get('price', 0.00):.2f}",
            "barcode": f"*DV{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}*"
        }
    
    def _generate_barcode_label_content(self, product: Dict[str, Any], template: str) -> Dict[str, Any]:
        """Generate barcode label content"""
        return {
            "barcode_value": product.get("upc", product.get("sku", product.get("id", "000000000000"))),
            "barcode_type": "UPC-A",
            "product_name": product.get("name", "Product")[:30],
            "sku": product.get("sku", product.get("id", "SKU")),
            "size": product.get("size", "Standard"),
            "color": product.get("color", "Default"),
            "human_readable": True
        }
    
    def _generate_warning_label_content(self, product: Dict[str, Any], template: str) -> Dict[str, Any]:
        """Generate warning label content"""
        warnings = product.get("warnings", ["General product warning"])
        
        return {
            "warning_text": warnings[0] if warnings else "CAUTION: Use as directed",
            "additional_warnings": warnings[1:] if len(warnings) > 1 else [],
            "product_name": product.get("name", "Product"),
            "warning_level": product.get("warning_level", "CAUTION"),
            "symbols": self._get_warning_symbols(product),
            "compliance_info": product.get("compliance", "See manual for details")
        }
    
    def _generate_generic_label_content(self, product: Dict[str, Any], template: str) -> Dict[str, Any]:
        """Generate generic label content"""
        return {
            "main_text": product.get("name", "Product Label"),
            "sub_text": product.get("description", "Product Description"),
            "identifier": product.get("id", "ID-UNKNOWN"),
            "date": datetime.now().strftime("%m/%d/%Y"),
            "barcode": self._generate_product_barcode(product)
        }
    
    def _generate_product_barcode(self, product: Dict[str, Any]) -> str:
        """Generate barcode for product"""
        # Use UPC if available, otherwise generate from product ID
        upc = product.get("upc")
        if upc:
            return upc
        
        # Generate from product ID
        product_id = str(product.get("id", "000000"))
        # Pad to 12 digits for UPC-A
        padded_id = product_id.zfill(12)
        return padded_id
    
    def _generate_product_qr_code(self, product: Dict[str, Any]) -> str:
        """Generate QR code data for product"""
        qr_data = {
            "id": product.get("id"),
            "name": product.get("name"),
            "price": product.get("price"),
            "url": f"https://dealvoy.com/products/{product.get('id', 'unknown')}"
        }
        return json.dumps(qr_data)
    
    def _get_warning_symbols(self, product: Dict[str, Any]) -> List[str]:
        """Get warning symbols for product"""
        category = product.get("category", "").lower()
        
        if "electronic" in category:
            return ["electrical_warning", "recycling"]
        elif "chemical" in category:
            return ["hazmat", "toxic", "corrosive"]
        elif "toy" in category:
            return ["choking_hazard", "age_restriction"]
        else:
            return ["general_caution"]
    
    def _get_label_dimensions(self, template: str) -> Dict[str, str]:
        """Get label dimensions for template"""
        dimensions = {
            "standard": {"width": "4.0in", "height": "2.0in"},
            "small": {"width": "2.0in", "height": "1.0in"},
            "large": {"width": "6.0in", "height": "4.0in"},
            "shipping": {"width": "4.0in", "height": "6.0in"},
            "price": {"width": "1.5in", "height": "1.0in"}
        }
        
        return dimensions.get(template, dimensions["standard"])
    
    def _get_print_settings(self, label_type: str, template: str) -> Dict[str, Any]:
        """Get print settings for label"""
        return {
            "dpi": 300,
            "color_mode": "color" if label_type in ["product", "custom"] else "monochrome",
            "paper_type": "label_stock",
            "orientation": "portrait",
            "margins": {"top": "0.1in", "bottom": "0.1in", "left": "0.1in", "right": "0.1in"}
        }
    
    def _format_label_output(self, labels: List[Dict[str, Any]], format_type: str) -> Dict[str, Any]:
        """Format label output based on format type"""
        if format_type == "pdf":
            return self._format_pdf_output(labels)
        elif format_type == "png":
            return self._format_image_output(labels, "png")
        elif format_type == "svg":
            return self._format_svg_output(labels)
        elif format_type == "html":
            return self._format_html_output(labels)
        elif format_type in ["zpl", "epl"]:
            return self._format_printer_output(labels, format_type)
        else:
            return {"error": f"Unsupported format: {format_type}"}
    
    def _format_pdf_output(self, labels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format labels as PDF"""
        # Simulate PDF generation
        pdf_content = f"PDF Content for {len(labels)} labels"
        
        return {
            "content_type": "application/pdf",
            "content": base64.b64encode(pdf_content.encode()).decode(),
            "size_bytes": len(pdf_content),
            "pages": (len(labels) + 3) // 4,  # 4 labels per page
            "labels_per_page": 4
        }
    
    def _format_image_output(self, labels: List[Dict[str, Any]], image_format: str) -> Dict[str, Any]:
        """Format labels as images"""
        images = []
        
        for i, label in enumerate(labels):
            image_data = f"Image data for label {i+1}"
            images.append({
                "label_id": label.get("product_id", f"label_{i+1}"),
                "content": base64.b64encode(image_data.encode()).decode(),
                "format": image_format,
                "size_bytes": len(image_data)
            })
        
        return {
            "content_type": f"image/{image_format}",
            "images": images,
            "total_images": len(images)
        }
    
    def _format_svg_output(self, labels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format labels as SVG"""
        svg_content = f'<svg><text>SVG content for {len(labels)} labels</text></svg>'
        
        return {
            "content_type": "image/svg+xml",
            "content": svg_content,
            "size_bytes": len(svg_content),
            "scalable": True
        }
    
    def _format_html_output(self, labels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format labels as HTML"""
        html_parts = ["<html><head><title>Product Labels</title></head><body>"]
        
        for label in labels:
            content = label.get("content", {})
            html_parts.append(f"<div class='label'>")
            html_parts.append(f"<h3>{content.get('title', 'Label')}</h3>")
            html_parts.append(f"<p>{content.get('description', '')}</p>")
            html_parts.append(f"<div class='barcode'>{content.get('barcode', '')}</div>")
            html_parts.append("</div>")
        
        html_parts.append("</body></html>")
        html_content = "\n".join(html_parts)
        
        return {
            "content_type": "text/html",
            "content": html_content,
            "size_bytes": len(html_content)
        }
    
    def _format_printer_output(self, labels: List[Dict[str, Any]], format_type: str) -> Dict[str, Any]:
        """Format labels for direct printer output (ZPL/EPL)"""
        commands = []
        
        for label in labels:
            if format_type == "zpl":
                command = self._generate_zpl_command(label)
            else:  # EPL
                command = self._generate_epl_command(label)
            commands.append(command)
        
        return {
            "content_type": "text/plain",
            "printer_commands": commands,
            "total_commands": len(commands),
            "printer_language": format_type.upper()
        }
    
    def _generate_zpl_command(self, label: Dict[str, Any]) -> str:
        """Generate ZPL command for label"""
        content = label.get("content", {})
        return f"^XA^FO50,50^A0N,50,50^FD{content.get('title', 'Label')}^FS^XZ"
    
    def _generate_epl_command(self, label: Dict[str, Any]) -> str:
        """Generate EPL command for label"""
        content = label.get("content", {})
        return f"A50,50,0,3,1,1,N,\"{content.get('title', 'Label')}\""
    
    def _generate_barcode(self, product: Dict[str, Any], barcode_type: str, include_text: bool, size: str) -> Dict[str, Any]:
        """Generate barcode for product"""
        barcode_value = self._generate_product_barcode(product)
        
        return {
            "product_id": product.get("id"),
            "barcode_type": barcode_type,
            "barcode_value": barcode_value,
            "include_text": include_text,
            "size": size,
            "dimensions": self._get_barcode_dimensions(size),
            "format": "png",
            "content": base64.b64encode(f"Barcode: {barcode_value}".encode()).decode()
        }
    
    def _get_barcode_dimensions(self, size: str) -> Dict[str, str]:
        """Get barcode dimensions by size"""
        sizes = {
            "small": {"width": "1.0in", "height": "0.5in"},
            "medium": {"width": "2.0in", "height": "1.0in"},
            "large": {"width": "3.0in", "height": "1.5in"}
        }
        
        return sizes.get(size, sizes["medium"])
    
    def _package_barcodes(self, barcodes: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
        """Package barcodes for delivery"""
        return {
            "package_type": "zip",
            "total_files": len(barcodes),
            "total_size_mb": sum(len(bc.get("content", "")) for bc in barcodes) / 1024 / 1024,
            "download_url": f"/downloads/barcodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        }
    
    def _generate_shipping_label_set(self, order: Dict[str, Any], carrier: str, label_size: str, include_return: bool) -> Dict[str, Any]:
        """Generate shipping label set for order"""
        tracking_number = f"{carrier.upper()}{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}"
        
        label_set = {
            "order_id": order.get("id", "ORDER-UNKNOWN"),
            "tracking_number": tracking_number,
            "carrier": carrier,
            "service": order.get("shipping_service", "Ground"),
            "shipping_label": {
                "sender": order.get("sender_address", {}),
                "recipient": order.get("shipping_address", {}),
                "package_info": {
                    "weight": f"{order.get('weight', 1.0)} lbs",
                    "dimensions": order.get("dimensions", "10x8x6 inches"),
                    "declared_value": f"${order.get('total', 0.00):.2f}"
                },
                "barcode": f"*{tracking_number}*",
                "label_format": label_size
            }
        }
        
        if include_return:
            return_tracking = f"RT{tracking_number[2:]}"
            label_set["return_label"] = {
                "tracking_number": return_tracking,
                "sender": order.get("shipping_address", {}),
                "recipient": order.get("sender_address", {}),
                "barcode": f"*{return_tracking}*"
            }
        
        return label_set
    
    def _generate_shipping_manifest(self, shipping_labels: List[Dict[str, Any]], carrier: str) -> Dict[str, Any]:
        """Generate shipping manifest"""
        return {
            "manifest_id": f"{carrier.upper()}_MAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "carrier": carrier,
            "total_shipments": len(shipping_labels),
            "total_weight": sum(float(label.get("shipping_label", {}).get("package_info", {}).get("weight", "1.0").split()[0]) for label in shipping_labels),
            "manifest_date": datetime.now().strftime("%Y-%m-%d"),
            "pickup_date": datetime.now().strftime("%Y-%m-%d"),
            "tracking_numbers": [label.get("tracking_number") for label in shipping_labels]
        }
    
    def _calculate_shipping_costs(self, shipping_labels: List[Dict[str, Any]], carrier: str) -> Dict[str, Any]:
        """Calculate shipping costs"""
        base_rate = {"ups": 8.50, "fedex": 9.00, "usps": 7.25}.get(carrier, 8.00)
        
        total_cost = 0
        costs_by_service = {}
        
        for label in shipping_labels:
            service = label.get("service", "Ground")
            weight = float(label.get("shipping_label", {}).get("package_info", {}).get("weight", "1.0").split()[0])
            
            # Simple cost calculation
            cost = base_rate * weight
            total_cost += cost
            
            if service not in costs_by_service:
                costs_by_service[service] = {"count": 0, "total_cost": 0}
            costs_by_service[service]["count"] += 1
            costs_by_service[service]["total_cost"] += cost
        
        return {
            "total_cost": round(total_cost, 2),
            "average_cost_per_shipment": round(total_cost / len(shipping_labels), 2),
            "costs_by_service": costs_by_service,
            "carrier": carrier
        }
    
    def _generate_tracking_info(self, shipping_labels: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate tracking information"""
        return [
            {
                "order_id": label.get("order_id"),
                "tracking_number": label.get("tracking_number"),
                "carrier": label.get("carrier"),
                "service": label.get("service"),
                "estimated_delivery": (datetime.now().replace(hour=0, minute=0, second=0) + 
                                     datetime.timedelta(days=random.randint(2, 7))).strftime("%Y-%m-%d")
            }
            for label in shipping_labels
        ]
    
    def _process_custom_template(self, template_config: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Process custom template configuration"""
        return {
            "template_name": template_config.get("name", "custom"),
            "layout": template_config.get("layout", "standard"),
            "fields": template_config.get("fields", []),
            "styling": {**template_config.get("styling", {}), **customizations.get("styling", {})},
            "dimensions": customizations.get("dimensions", template_config.get("dimensions", {}))
        }
    
    def _apply_template_to_data(self, template: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply template to data item"""
        label_content = {}
        
        for field in template.get("fields", []):
            field_name = field.get("name")
            field_source = field.get("source", field_name)
            
            if field_source in data:
                label_content[field_name] = data[field_source]
            else:
                label_content[field_name] = field.get("default", "")
        
        return {
            "template": template["template_name"],
            "content": label_content,
            "styling": template.get("styling", {}),
            "dimensions": template.get("dimensions", {})
        }
    
    def _validate_custom_labels(self, labels: List[Dict[str, Any]], template_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate custom labels"""
        required_fields = template_config.get("required_fields", [])
        validation_errors = []
        
        for i, label in enumerate(labels):
            content = label.get("content", {})
            for field in required_fields:
                if not content.get(field):
                    validation_errors.append(f"Label {i+1}: Missing required field '{field}'")
        
        return {
            "total_labels": len(labels),
            "validation_errors": validation_errors,
            "valid_labels": len(labels) - len(validation_errors),
            "validation_passed": len(validation_errors) == 0
        }
    
    def _calculate_label_statistics(self, labels: List[Dict[str, Any]], formatted_output: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate label generation statistics"""
        return {
            "total_labels_generated": len(labels),
            "output_size_bytes": formatted_output.get("size_bytes", 0),
            "output_size_mb": round(formatted_output.get("size_bytes", 0) / 1024 / 1024, 2),
            "labels_with_barcodes": len([l for l in labels if l.get("content", {}).get("barcode")]),
            "unique_products": len(set(l.get("product_id") for l in labels))
        }
    
    def _generate_print_instructions(self, config: Dict[str, Any], statistics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate printing instructions"""
        return {
            "recommended_printer": "Label printer or standard inkjet/laser",
            "paper_type": "Label stock or regular paper",
            "print_quality": "300 DPI minimum",
            "color_mode": "Color recommended for product labels",
            "labels_per_page": 4 if config.get("label_type") == "product" else 1,
            "estimated_pages": (statistics["total_labels_generated"] + 3) // 4,
            "print_order": "Sequential by product ID"
        }
    
    def run(self, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main execution method"""
        input_data = input_data or {}
        
        operation = input_data.get("operation", "status")
        
        if operation == "generate_labels" and "label_config" in input_data:
            return self.generate_product_labels(input_data["label_config"])
        elif operation == "generate_barcodes" and "barcode_config" in input_data:
            return self.generate_barcodes(input_data["barcode_config"])
        elif operation == "generate_shipping" and "shipping_config" in input_data:
            return self.generate_shipping_labels(input_data["shipping_config"])
        elif operation == "generate_custom" and "custom_config" in input_data:
            return self.generate_custom_labels(input_data["custom_config"])
        
        return {
            "status": "ready",
            "agent": self.agent_name,
            "capabilities": ["product_labels", "barcodes", "shipping_labels", "custom_labels"],
            "supported_formats": self.formats,
            "label_types": self.label_types
        }

if __name__ == "__main__":
    agent = LabelGenerator()
    print(json.dumps(agent.run(), indent=2))
