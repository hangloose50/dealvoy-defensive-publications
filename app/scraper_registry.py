# app/services/scraper_registry.py

from typing import Callable
from app.schemas import PriceSnapshot

# Maps scraper names to functions: (upc: str) -> PriceSnapshot
registry: dict[str, Callable[[str], PriceSnapshot]] = {}

def register(func: Callable[[str], PriceSnapshot]) -> Callable[[str], PriceSnapshot]:
    """
    Decorator to register a scraper function.
    Usage:
       @register
       def amazon(upc: str) -> PriceSnapshot: ...
    """
    registry[func.__name__] = func
    return func

