import anthropic
from app.config import settings
from app.utils.logger import logger
from app.models import AdData
from typing import List
import json

class ClaudeService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
    
    async def analyze_ads(
        self,
        ads: List[AdData],
        analysis_prompt: str
    ) -> str:
        try:
            logger.info(f"Analyzing {len(ads)} ads with Claude")
            
            ads_json = json.dumps([
                {
                    "page": ad.page_name,
                    "id": ad.ad_id,
                    "impressions": ad.impressions,
                    "spend": ad.spend,
                    "text": ad.text,
                    "platforms": ad.platforms
                }
                for ad in ads
            ], indent=2)
            
            prompt = f"""You are an expert marketing analyst. Analyze the following Meta ads and provide insights.

Analysis Request: {analysis_prompt}

Ad Data:
{ads_json}

Provide a comprehensive analysis including:
1. Key patterns and trends
2. Marketing strategies observed
3. Target audience insights
4. Creative elements used
5. Recommendations based on findings"""
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis = message.content[0].text
            logger.info("Analysis completed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing with Claude: {e}")
            raise
    
    def get_model_info(self) -> dict:
        return {
            "model": self.model,
            "provider": "Anthropic",
            "capabilities": ["text-analysis", "pattern-recognition", "insights"]
        }
