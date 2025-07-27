# test_orchestration.py

import pytest
from app import asyncio
from app.orchestration import run_scrapers, filter_by_roi, SCRAPER_REGISTRY

@pytest.fixture(autouse=True)
def patch_scrapers(monkeypatch):
    async def mock_scrape_foo():
        return [{"price": 10, "amazon_price": 15}]
    async def mock_scrape_bar():
        return [{"price": 20, "amazon_price": 18}]
    # override registry entries for Foo and Bar
    monkeypatch.setitem(SCRAPER_REGISTRY, "Foo", mock_scrape_foo)
    monkeypatch.setitem(SCRAPER_REGISTRY, "Bar", mock_scrape_bar)

@pytest.mark.asyncio
async def test_run_scrapers_returns_all_items():
    items = await run_scrapers(["Foo", "Bar"])
    assert items == [
        {"price": 10, "amazon_price": 15},
        {"price": 20, "amazon_price": 18},
    ]

def test_filter_by_roi_filters_items():
    items = [
        {"price": 10, "amazon_price": 15},  # ROI = 50%
        {"price": 20, "amazon_price": 18},  # ROI = -10%
    ]
    filtered = filter_by_roi(items, threshold=20)
    assert filtered == [
        {"price": 10, "amazon_price": 15},
    ]

@pytest.mark.asyncio
async def test_run_and_filter_pipeline():
    items = await run_scrapers(["Foo", "Bar"])
    filtered = filter_by_roi(items, threshold=30)
    assert filtered == [
        {"price": 10, "amazon_price": 15},
    ]
