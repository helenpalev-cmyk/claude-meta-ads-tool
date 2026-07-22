import pytest
from app.services.meta_ads_service import MetaAdsService
from app.services.claude_service import ClaudeService

class TestMetaAdsService:
    def test_validate_country_code_valid(self):
        assert MetaAdsService.validate_country_code("US") == True
        assert MetaAdsService.validate_country_code("UK") == True
        assert MetaAdsService.validate_country_code("CA") == True
    
    def test_validate_country_code_invalid(self):
        assert MetaAdsService.validate_country_code("XX") == False
        assert MetaAdsService.validate_country_code("INVALID") == False

class TestClaudeService:
    def test_claude_service_init(self):
        service = ClaudeService()
        assert service.client is not None
        assert service.model == "claude-3-5-sonnet-20241022"
