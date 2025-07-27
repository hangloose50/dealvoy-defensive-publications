# test_export.py

import pytest
import test_quests

@pytest.mark.integration
def test_export_webhook():
    # your existing test logic that hits 127.0.0.1:8000
    response = requests.post("http://127.0.0.1:8000/api/v1/webhook/export", json={"data": "x"})
    assert response.status_code == 200

import test_quests
import test_

API_KEY = os.getenv("EXPORT_API_KEY", "dev-token")  # Or paste it directly here
WEBHOOK_ID = "9ad6fad2-ffa1-4303-b471-89a91fd32d43"

payload = {
    "webhook_id": WEBHOOK_ID,
    "items": [
        { "upc": "12345", "price": 11.99, "roi": 0.34 },
        { "upc": "67890", "price": 8.49,  "roi": 0.22 }
    ]
}

response = requests.post(
    "http://127.0.0.1:8000/api/v1/webhook/export",
    json=payload,
    headers={"X-API-KEY": API_KEY}
)

print("Status:", response.status_code)
print("Response:", response.json())


