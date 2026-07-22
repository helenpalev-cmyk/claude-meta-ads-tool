import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

class TestAdsEndpoints:
    def test_search_ads_missing_query(self):
        response = client.post("/api/v1/ads/search", json={
            "query": "",
            "country": "US",
            "max_results": 10
        })
        assert response.status_code == 400
    
    def test_analyze_ads_missing_prompt(self):
        response = client.post("/api/v1/ads/analyze", json={
            "query": "test",
            "country": "US",
            "max_results": 5,
            "analysis_prompt": ""
        })
        assert response.status_code == 400
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
