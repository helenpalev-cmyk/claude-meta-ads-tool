from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SearchAdsRequest(BaseModel):
    query: str = Field(..., description="Search query for ads")
    country: str = Field(default="US", description="Country code (US, UK, CA, etc.)")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum ads to return")

class AnalyzeAdsRequest(BaseModel):
    query: str = Field(..., description="Search query for ads")
    country: str = Field(default="US", description="Country code")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum ads to analyze")
    analysis_prompt: str = Field(..., description="What to analyze in the ads")

class AdData(BaseModel):
    page_name: str
    ad_id: str
    impressions: Optional[str] = None
    spend: Optional[str] = None
    text: Optional[str] = None
    platforms: Optional[List[str]] = None

class SearchAdsResponse(BaseModel):
    success: bool
    ads: List[AdData]
    count: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None

class AnalyzeAdsResponse(BaseModel):
    success: bool
    ads: List[AdData]
    analysis: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
