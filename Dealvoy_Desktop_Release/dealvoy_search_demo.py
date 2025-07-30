#!/usr/bin/env python3
"""
Dealvoy Enhanced Search Demo
Demonstrates 50+ source integration capabilities
"""

from enhanced_retail_integration import EnhancedRetailSourceFinder

def main():
    print("🚀 Dealvoy Enhanced Product Search")
    print("=" * 50)
    
    # Initialize the enhanced finder
    finder = EnhancedRetailSourceFinder()
    
    # Show available sources
    info = finder.get_source_info()
    print(f"📊 {info['total_sources']} sources available across {len(info['categories'])} categories")
    
    # Interactive search
    while True:
        query = input("\n🔍 Enter search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        
        print(f"Searching for: {query}")
        results = finder.find_products(query, max_results=20)
        
        print(f"\n📋 Results Summary:")
        print(f"  Total Products Found: {results['combined_count']}")
        print(f"  Sources Searched: {len(results['sources_used'])}")
        
        # Show results by source
        if results['new_results']:
            print(f"\n🌐 New Source Results:")
            for source, products in results['new_results'].items():
                print(f"  {source}: {len(products)} products")
                for i, product in enumerate(products[:3], 1):  # Show first 3
                    print(f"    {i}. {product['title'][:50]}... (${product['price']})")

if __name__ == "__main__":
    main()
