#!/usr/bin/env python3
"""
Enhanced Retail Scraper Registry - Manages 50+ retail source scrapers
Provides centralized access to all scraper modules with compliance tracking
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional, Any
from dataclasses import asdict

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

class ScraperRegistry:
    """
    Central registry for managing all retail scrapers
    """
    
    def __init__(self):
        self.scrapers = {}
        self.scraper_stats = {}
        self._load_scrapers()
    
    def _load_scrapers(self):
        """Load all available scrapers"""
        scraper_configs = [
            # Major Retailers
            {
                'name': 'target',
                'module': 'target_scraper',
                'class': 'TargetScraper',
                'function': 'scrape_target',
                'category': 'General Retail',
                'description': 'Target.com - General merchandise, electronics, home goods'
            },
            {
                'name': 'bestbuy',
                'module': 'bestbuy_scraper',
                'class': 'BestBuyScraper',
                'function': 'scrape_bestbuy',
                'category': 'Electronics',
                'description': 'BestBuy.com - Electronics, appliances, tech products'
            },
            {
                'name': 'cvs',
                'module': 'cvs_scraper',
                'class': 'CVSScraper',
                'function': 'scrape_cvs',
                'category': 'Health & Beauty',
                'description': 'CVS.com - Pharmacy, health, beauty products'
            },
            {
                'name': 'homedepot',
                'module': 'homedepot_scraper',
                'class': 'HomeDepotScraper',
                'function': 'scrape_homedepot',
                'category': 'Home Improvement',
                'description': 'HomeDepot.com - Tools, hardware, building materials'
            },
            {
                'name': 'lowes',
                'module': 'lowes_scraper',
                'class': 'LowesScraper',
                'function': 'scrape_lowes',
                'category': 'Home Improvement',
                'description': 'Lowes.com - Home improvement, appliances, tools'
            },
            
            # Electronics & Tech
            {
                'name': 'newegg',
                'module': 'newegg_scraper',
                'class': 'NeweggScraper',
                'function': 'scrape_newegg',
                'category': 'Electronics',
                'description': 'Newegg.com - Computer hardware, electronics'
            },
            {
                'name': 'microcenter',
                'module': 'microcenter_scraper',
                'class': 'MicroCenterScraper',
                'function': 'scrape_microcenter',
                'category': 'Electronics',
                'description': 'MicroCenter.com - Computer parts, electronics'
            },
            {
                'name': 'frys',
                'module': 'frys_scraper',
                'class': 'FrysScraper',
                'function': 'scrape_frys',
                'category': 'Electronics',
                'description': 'Frys.com - Electronics, appliances'
            },
            
            # Department Stores
            {
                'name': 'macys',
                'module': 'macys_scraper',
                'class': 'MacysScraper',
                'function': 'scrape_macys',
                'category': 'Department Store',
                'description': 'Macys.com - Clothing, home goods, beauty'
            },
            {
                'name': 'nordstrom',
                'module': 'nordstrom_scraper',
                'class': 'NordstromScraper',
                'function': 'scrape_nordstrom',
                'category': 'Department Store',
                'description': 'Nordstrom.com - Fashion, shoes, accessories'
            },
            {
                'name': 'kohls',
                'module': 'kohls_scraper',
                'class': 'KohlsScraper',
                'function': 'scrape_kohls',
                'category': 'Department Store',
                'description': 'Kohls.com - Clothing, home, beauty'
            },
            
            # Specialty Stores
            {
                'name': 'rei',
                'module': 'rei_scraper',
                'class': 'REIScraper',
                'function': 'scrape_rei',
                'category': 'Outdoor',
                'description': 'REI.com - Outdoor gear, camping, sports equipment'
            },
            {
                'name': 'gamestop',
                'module': 'gamestop_scraper',
                'class': 'GameStopScraper',
                'function': 'scrape_gamestop',
                'category': 'Gaming',
                'description': 'GameStop.com - Video games, gaming accessories'
            },
            {
                'name': 'petco',
                'module': 'petco_scraper',
                'class': 'PetcoScraper',
                'function': 'scrape_petco',
                'category': 'Pet Supplies',
                'description': 'Petco.com - Pet food, supplies, accessories'
            },
            {
                'name': 'petsmart',
                'module': 'petsmart_scraper',
                'class': 'PetSmartScraper',
                'function': 'scrape_petsmart',
                'category': 'Pet Supplies',
                'description': 'PetSmart.com - Pet supplies, grooming, food'
            },
            {
                'name': 'staples',
                'module': 'staples_scraper',
                'class': 'StaplesScraper',
                'function': 'scrape_staples',
                'category': 'Office Supplies',
                'description': 'Staples.com - Office supplies, electronics, furniture'
            },
            {
                'name': 'officedepot',
                'module': 'officedepot_scraper',
                'class': 'OfficeDepotScraper',
                'function': 'scrape_officedepot',
                'category': 'Office Supplies',
                'description': 'OfficeDepot.com - Office supplies, technology'
            },
            
            # Fashion & Apparel
            {
                'name': 'gap',
                'module': 'gap_scraper',
                'class': 'GapScraper',
                'function': 'scrape_gap',
                'category': 'Fashion',
                'description': 'Gap.com - Clothing, accessories'
            },
            {
                'name': 'oldnavy',
                'module': 'oldnavy_scraper',
                'class': 'OldNavyScraper',
                'function': 'scrape_oldnavy',
                'category': 'Fashion',
                'description': 'OldNavy.com - Affordable clothing, family fashion'
            },
            {
                'name': 'nike',
                'module': 'nike_scraper',
                'class': 'NikeScraper',
                'function': 'scrape_nike',
                'category': 'Sportswear',
                'description': 'Nike.com - Athletic wear, shoes, equipment'
            },
            {
                'name': 'adidas',
                'module': 'adidas_scraper',
                'class': 'AdidasScraper',
                'function': 'scrape_adidas',
                'category': 'Sportswear',
                'description': 'Adidas.com - Athletic wear, shoes, sports gear'
            },
            
            # Beauty & Personal Care
            {
                'name': 'sephora',
                'module': 'sephora_scraper',
                'class': 'SephoraScraper',
                'function': 'scrape_sephora',
                'category': 'Beauty',
                'description': 'Sephora.com - Cosmetics, skincare, fragrance'
            },
            {
                'name': 'ulta',
                'module': 'ulta_scraper',
                'class': 'UltaScraper',
                'function': 'scrape_ulta',
                'category': 'Beauty',
                'description': 'Ulta.com - Beauty products, salon services'
            },
            
            # Grocery & Food
            {
                'name': 'kroger',
                'module': 'kroger_scraper',
                'class': 'KrogerScraper',
                'function': 'scrape_kroger',
                'category': 'Grocery',
                'description': 'Kroger.com - Groceries, household items'
            },
            {
                'name': 'safeway',
                'module': 'safeway_scraper',
                'class': 'SafewayScraper',
                'function': 'scrape_safeway',
                'category': 'Grocery',
                'description': 'Safeway.com - Groceries, pharmacy, deli'
            },
            {
                'name': 'foodlion',
                'module': 'foodlion_scraper',
                'class': 'FoodLionScraper',
                'function': 'scrape_foodlion',
                'category': 'Grocery',
                'description': 'FoodLion.com - Groceries, fresh food, bakery'
            },
            {
                'name': 'giant',
                'module': 'giant_scraper',
                'class': 'GiantScraper',
                'function': 'scrape_giant',
                'category': 'Grocery',
                'description': 'GiantFood.com - Groceries, deli, bakery'
            },
            {
                'name': 'worldmarket',
                'module': 'worldmarket_scraper',
                'class': 'WorldMarketScraper',
                'function': 'scrape_worldmarket',
                'category': 'Grocery',
                'description': 'WorldMarket.com - International foods, home goods'
            },
            {
                'name': 'wholefoods',
                'module': 'wholefoods_scraper',
                'class': 'WholeFoodsScraper',
                'function': 'scrape_wholefoods',
                'category': 'Grocery',
                'description': 'WholeFoods.com - Organic groceries, natural products'
            },
            
            # Automotive
            {
                'name': 'autozone',
                'module': 'autozone_scraper',
                'class': 'AutoZoneScraper',
                'function': 'scrape_autozone',
                'category': 'Automotive',
                'description': 'AutoZone.com - Auto parts, accessories, tools'
            },
            {
                'name': 'pepboys',
                'module': 'pepboys_scraper',
                'class': 'PepBoysScraper',
                'function': 'scrape_pepboys',
                'category': 'Automotive',
                'description': 'PepBoys.com - Auto parts, tires, services'
            },
            
            # Specialty Categories
            {
                'name': 'hobbbylobby',
                'module': 'hobbylobby_scraper',
                'class': 'HobbyLobbyScraper',
                'function': 'scrape_hobbylobby',
                'category': 'Crafts',
                'description': 'HobbyLobby.com - Arts, crafts, home decor'
            },
            {
                'name': 'michaels',
                'module': 'michaels_scraper',
                'class': 'MichaelsScraper',
                'function': 'scrape_michaels',
                'category': 'Crafts',
                'description': 'Michaels.com - Arts, crafts, party supplies'
            },
            {
                'name': 'ikea',
                'module': 'ikea_scraper',
                'class': 'IkeaScraper',
                'function': 'scrape_ikea',
                'category': 'Furniture',
                'description': 'IKEA.com - Furniture, home goods, decor'
            },
            {
                'name': 'wayfair',
                'module': 'wayfair_scraper',
                'class': 'WayfairScraper',
                'function': 'scrape_wayfair',
                'category': 'Furniture',
                'description': 'Wayfair.com - Furniture, home decor, appliances'
            },
            
            # Bookstores
            {
                'name': 'barnesnoble',
                'module': 'barnesnoble_scraper',
                'class': 'BarnesNobleScraper',
                'function': 'scrape_barnesnoble',
                'category': 'Books',
                'description': 'BarnesAndNoble.com - Books, games, gifts'
            },
            
            # Musical Instruments
            {
                'name': 'guitarcenter',
                'module': 'guitarcenter_scraper',
                'class': 'GuitarCenterScraper',
                'function': 'scrape_guitarcenter',
                'category': 'Music',
                'description': 'GuitarCenter.com - Musical instruments, audio equipment'
            },
            
            # Pharmacy Chains
            {
                'name': 'walgreens',
                'module': 'walgreens_scraper',
                'class': 'WalgreensScraper',
                'function': 'scrape_walgreens',
                'category': 'Pharmacy',
                'description': 'Walgreens.com - Pharmacy, health, beauty'
            },
            {
                'name': 'riteaid',
                'module': 'riteaid_scraper',
                'class': 'RiteAidScraper',
                'function': 'scrape_riteaid',
                'category': 'Pharmacy',
                'description': 'RiteAid.com - Pharmacy, wellness products'
            },
            
            # Sporting Goods
            {
                'name': 'dickssportinggoods',
                'module': 'dickssportinggoods_scraper',
                'class': 'DicksSportingGoodsScraper',
                'function': 'scrape_dickssportinggoods',
                'category': 'Sporting Goods',
                'description': 'DicksSportingGoods.com - Sports equipment, apparel'
            },
            {
                'name': 'bigfive',
                'module': 'bigfive_scraper',
                'class': 'BigFiveScraper',
                'function': 'scrape_bigfive',
                'category': 'Sporting Goods',
                'description': 'BigFive.com - Sporting goods, outdoor gear'
            },
            
            # Wholesale Clubs
            {
                'name': 'samsclub',
                'module': 'samsclub_scraper',
                'class': 'SamsClubScraper',
                'function': 'scrape_samsclub',
                'category': 'Wholesale',
                'description': 'SamsClub.com - Wholesale, bulk items'
            },
            {
                'name': 'bjs',
                'module': 'bjs_scraper',
                'class': 'BJSScraper',
                'function': 'scrape_bjs',
                'category': 'Wholesale',
                'description': 'BJs.com - Warehouse club, bulk items'
            },
            
            # Additional Major Retailers
            {
                'name': 'jcpenney',
                'module': 'jcpenney_scraper',
                'class': 'JCPenneyScraper',
                'function': 'scrape_jcpenney',
                'category': 'Department Store',
                'description': 'JCPenney.com - Clothing, home, jewelry'
            },
            {
                'name': 'overstock',
                'module': 'overstock_scraper',
                'class': 'OverstockScraper',
                'function': 'scrape_overstock',
                'category': 'General Retail',
                'description': 'Overstock.com - Home goods, furniture, jewelry'
            },
            {
                'name': 'qvc',
                'module': 'qvc_scraper',
                'class': 'QVCScraper',
                'function': 'scrape_qvc',
                'category': 'General Retail',
                'description': 'QVC.com - Home shopping, electronics, fashion'
            },
            {
                'name': 'hsn',
                'module': 'hsn_scraper',
                'class': 'HSNScraper',
                'function': 'scrape_hsn',
                'category': 'General Retail',
                'description': 'HSN.com - Home shopping network products'
            },
            
            # Dollar Stores
            {
                'name': 'dollartree',
                'module': 'dollartree_scraper',
                'class': 'DollarTreeScraper',
                'function': 'scrape_dollartree',
                'category': 'Discount',
                'description': 'DollarTree.com - Discount items, household goods'
            },
            {
                'name': 'dollargeneral',
                'module': 'dollargeneral_scraper',
                'class': 'DollarGeneralScraper',
                'function': 'scrape_dollargeneral',
                'category': 'Discount',
                'description': 'DollarGeneral.com - Convenience items, household goods'
            },
            
            # Tech Specialty
            {
                'name': 'apple',
                'module': 'apple_scraper',
                'class': 'AppleScraper',
                'function': 'scrape_apple',
                'category': 'Electronics',
                'description': 'Apple.com - Apple products, accessories'
            },
            {
                'name': 'microsoft',
                'module': 'microsoft_scraper',
                'class': 'MicrosoftScraper',
                'function': 'scrape_microsoft',
                'category': 'Electronics',
                'description': 'Microsoft.com - Microsoft products, software'
            }
        ]
        
        # Register all scrapers
        for config in scraper_configs:
            self.scrapers[config['name']] = config
            self.scraper_stats[config['name']] = {
                'total_requests': 0,
                'successful_requests': 0,
                'last_used': None,
                'compliance_status': 'unknown'
            }
    
    def get_scraper(self, source_name: str):
        """Get a specific scraper instance"""
        if source_name not in self.scrapers:
            return None
        
        config = self.scrapers[source_name]
        try:
            # Dynamic import
            module = __import__(config['module'])
            scraper_class = getattr(module, config['class'])
            return scraper_class()
        except (ImportError, AttributeError) as e:
            print(f"❌ Failed to load scraper {source_name}: {str(e)}")
            return None
    
    def get_scraper_function(self, source_name: str):
        """Get the scraper function for a source"""
        if source_name not in self.scrapers:
            return None
        
        config = self.scrapers[source_name]
        try:
            # Dynamic import
            module = __import__(config['module'])
            scraper_function = getattr(module, config['function'])
            return scraper_function
        except (ImportError, AttributeError) as e:
            print(f"❌ Failed to load scraper function {source_name}: {str(e)}")
            return None
    
    def search_all_sources(self, query: str, max_results_per_source: int = 5, 
                          categories: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        """Search across multiple sources"""
        results = {}
        
        # Filter scrapers by category if specified
        scrapers_to_use = []
        for name, config in self.scrapers.items():
            if categories is None or config['category'] in categories:
                scrapers_to_use.append(name)
        
        print(f"🔍 Searching {len(scrapers_to_use)} sources for: {query}")
        
        for source_name in scrapers_to_use:
            try:
                scraper_func = self.get_scraper_function(source_name)
                if scraper_func:
                    print(f"  🌐 Searching {source_name}...")
                    products = scraper_func(query, max_results_per_source)
                    if products:
                        results[source_name] = products
                        self._update_stats(source_name, True)
                    else:
                        self._update_stats(source_name, False)
                        
                    # Rate limiting between sources
                    time.sleep(1)
                    
            except Exception as e:
                print(f"❌ Error searching {source_name}: {str(e)}")
                self._update_stats(source_name, False)
        
        return results
    
    def get_available_sources(self) -> List[str]:
        """Get list of all available scraper sources"""
        return list(self.scrapers.keys())
    
    def get_sources_by_category(self, category: str) -> List[str]:
        """Get sources filtered by category"""
        return [name for name, config in self.scrapers.items() 
                if config['category'] == category]
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        return list(set(config['category'] for config in self.scrapers.values()))
    
    def _update_stats(self, source_name: str, success: bool):
        """Update scraper statistics"""
        if source_name in self.scraper_stats:
            stats = self.scraper_stats[source_name]
            stats['total_requests'] += 1
            if success:
                stats['successful_requests'] += 1
            stats['last_used'] = time.time()
    
    def get_scraper_info(self, source_name: str) -> Dict[str, Any]:
        """Get detailed information about a scraper"""
        if source_name not in self.scrapers:
            return {}
        
        config = self.scrapers[source_name].copy()
        config.update(self.scraper_stats[source_name])
        return config
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get overall registry statistics"""
        total_scrapers = len(self.scrapers)
        categories = self.get_all_categories()
        
        category_counts = {}
        for category in categories:
            category_counts[category] = len(self.get_sources_by_category(category))
        
        return {
            'total_scrapers': total_scrapers,
            'categories': categories,
            'category_counts': category_counts,
            'scrapers': list(self.scrapers.keys())
        }

# Global registry instance
registry = ScraperRegistry()

def search_products(query: str, sources: Optional[List[str]] = None, 
                   categories: Optional[List[str]] = None, 
                   max_results_per_source: int = 5) -> Dict[str, List[dict]]:
    """
    Main function to search products across multiple retail sources
    
    Args:
        query: Search query
        sources: Specific sources to search (optional)
        categories: Categories to filter by (optional)
        max_results_per_source: Max results per source
    
    Returns:
        Dictionary with source names as keys and product lists as values
    """
    if sources:
        # Search specific sources
        results = {}
        for source in sources:
            if source in registry.scrapers:
                scraper_func = registry.get_scraper_function(source)
                if scraper_func:
                    try:
                        products = scraper_func(query, max_results_per_source)
                        if products:
                            results[source] = products
                    except Exception as e:
                        print(f"❌ Error searching {source}: {str(e)}")
        return results
    else:
        # Search all sources or by category
        return registry.search_all_sources(query, max_results_per_source, categories)

def get_available_sources() -> List[str]:
    """Get list of all available scraper sources"""
    return registry.get_available_sources()

def get_registry_info() -> Dict[str, Any]:
    """Get comprehensive registry information"""
    return registry.get_registry_stats()

def demo_registry():
    """Demo the scraper registry system"""
    print("🌐 Retail Scraper Registry Demo")
    print("=" * 50)
    
    # Show registry stats
    stats = get_registry_info()
    print(f"📊 Total Scrapers: {stats['total_scrapers']}")
    print(f"📂 Categories: {', '.join(stats['categories'])}")
    
    # Demo searches
    print(f"\n🔍 Testing searches across categories...")
    
    # Test electronics category
    print(f"\n🖥️  Electronics Category:")
    electronics_results = search_products("laptop", categories=["Electronics"], max_results_per_source=2)
    for source, products in electronics_results.items():
        print(f"  {source}: {len(products)} products found")
    
    # Test specific sources
    print(f"\n🎯 Testing specific sources:")
    specific_results = search_products("headphones", sources=["target", "bestbuy"], max_results_per_source=3)
    for source, products in specific_results.items():
        print(f"  {source}: {len(products)} products found")

if __name__ == "__main__":
    demo_registry()
