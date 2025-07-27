# http_utils.py


import time
import random
import sys
import logging
import yaml
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Any, Dict, List

# ensure that print outputs never fail on Unicode
if hasattr(sys.stdout, "reconfigure"):
    # type: ignore[attr-defined]
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load_config(path: str = "config.yml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config: Dict[str, Any] = load_config()

user_agents: List[str] = config.get("user_agents", [])
proxy_endpoints: List[str] = config.get("proxies", [])
default_headers: Dict[str, str] = {"Accept-Language": "en-US,en;q=0.9"}

def fetch_with_retries(
    url: str,
    extra_headers: Optional[Dict[str, str]] = None,
    session: Optional[requests.Session] = None
):
    """
    Retrieve a URL, retrying on failure with exponential backoff,
    rotating User-Agent and optional proxies.
    """
    session = session or requests.Session()
    retries: int = int(config["http"]["max_retries"])
    backoff_power: float = float(config["http"]["backoff_factor"])
    timeout: float = float(config["http"]["timeout"])

    for attempt in range(1, retries + 1):
        ua: str = random.choice(user_agents)
        headers: Dict[str, str] = {**default_headers, "User-Agent": ua}
        if extra_headers:
            headers.update(extra_headers)

        proxy_cfg: Optional[Dict[str, str]] = None
        if proxy_endpoints:
            proxy: str = random.choice(proxy_endpoints)
            proxy_cfg = {"http": proxy, "https": proxy}

        try:
            response = session.get(
                url,
                headers=headers,
                proxies=proxy_cfg,
                timeout=timeout
            )
            if response.status_code == 200:
                return response

            wait = (backoff_power ** attempt) + random.random()
            logging.warning(f"{response.status_code} from {url}, retrying in {wait:.1f}s")
            time.sleep(wait)

        except Exception as err:
            wait = (backoff_power ** attempt) + random.random()
            logging.error(f"{err} fetching {url}, retrying in {wait:.1f}s")
            time.sleep(wait)

    logging.error(f"Gave up on {url} after {retries} attempts")
    return None

def fetch_concurrent(
    urls: List[str],
    max_workers: Optional[int] = None,
    **kwargs: Any
) -> List[tuple[str, Optional[requests.Response]]]:
    """
    Fetch multiple URLs in parallel using ThreadPoolExecutor.
    Returns list of (url, response_or_None).
    """
    max_workers = max_workers or int(config["concurrency"]["max_workers"])
    results: List[tuple[str, Optional[requests.Response]]] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fetch_with_retries, url, **kwargs): url
            for url in urls
        }
        for future in as_completed(futures):
            url = futures[future]
            response = future.result()
            results.append((url, response))
            # jitter to avoid request bursts
            time.sleep(random.uniform(0.1, 0.3))
    return results

def get_json(url: str) -> Optional[Dict[str, Any]]:
    """
    Helper function to fetch a URL and return its JSON response if successful.
    """
    response = fetch_with_retries(url)
    if response and response.ok:
        try:
            return response.json()
        except Exception as err:
            logging.error(f"Error decoding JSON from {url}: {err}")
    return None







