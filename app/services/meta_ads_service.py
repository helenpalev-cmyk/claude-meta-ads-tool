from meta_ads_collector import MetaAdsCollector
from app.utils.logger import logger
from app.models import AdData
from typing import List
import asyncio

class MetaAdsService:
    @staticmethod
    async def search_ads(
        query: str,
        country: str = "US",
        max_results: int = 10
    ) -> List[AdData]:
        try:
            logger.info(f"Searching Meta ads: query={query}, country={country}")
            
            def _collect_ads():
                collected = []
                with MetaAdsCollector() as collector:
                    for ad in collector.search(query=query, country=country, max_results=max_results):
                        try:
                            ad_data = AdData(
                                page_name=ad.page.name if ad.page else "Unknown",
                                ad_id=str(ad.id),
                                impressions=getattr(ad, 'impressions', None),
                                spend=getattr(ad, 'spend', None),
                                text=str(ad.text)[:150] if hasattr(ad, 'text') and ad.text else None,
                                platforms=getattr(ad, 'platforms', None)
                            )
                            collected.append(ad_data)
                        except Exception as e:
                            logger.warning(f"Error processing ad: {e}")
                            continue
                return collected
            
            loop = asyncio.get_event_loop()
            ads = await loop.run_in_executor(None, _collect_ads)
            logger.info(f"Found {len(ads)} ads")
            return ads
            
        except Exception as e:
            logger.error(f"Error searching Meta ads: {e}")
            raise
    
    @staticmethod
    def validate_country_code(country: str) -> bool:
        valid_countries = ["US", "UK", "CA", "AU", "DE", "FR", "IT", "ES", "BR", "MX", "IN", "JP", "CN", "RU", "ZA", "NZ"]
        return country.upper() in valid_countries
