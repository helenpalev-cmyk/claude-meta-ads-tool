from fastapi import APIRouter, HTTPException, status
from app.models import (
    SearchAdsRequest,
    AnalyzeAdsRequest,
    SearchAdsResponse,
    AnalyzeAdsResponse
)
from app.services.meta_ads_service import MetaAdsService
from app.services.claude_service import ClaudeService
from app.utils.logger import logger

router = APIRouter(prefix="/ads", tags=["ads"])
meta_service = MetaAdsService()
claude_service = ClaudeService()

@router.post("/search", response_model=SearchAdsResponse)
async def search_ads(request: SearchAdsRequest) -> SearchAdsResponse:
    try:
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )
        
        logger.info(f"Search request: {request.query}")
        
        ads = await meta_service.search_ads(
            query=request.query,
            country=request.country,
            max_results=request.max_results
        )
        
        if not ads:
            return SearchAdsResponse(
                success=True,
                ads=[],
                count=0,
                error="No ads found for the given query"
            )
        
        return SearchAdsResponse(
            success=True,
            ads=ads,
            count=len(ads)
        )
        
    except Exception as e:
        logger.error(f"Error in search_ads: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching ads: {str(e)}"
        )

@router.post("/analyze", response_model=AnalyzeAdsResponse)
async def analyze_ads(request: AnalyzeAdsRequest) -> AnalyzeAdsResponse:
    try:
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )
        
        if not request.analysis_prompt or len(request.analysis_prompt.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Analysis prompt cannot be empty"
            )
        
        logger.info(f"Analyze request: {request.query}")
        
        ads = await meta_service.search_ads(
            query=request.query,
            country=request.country,
            max_results=request.max_results
        )
        
        if not ads:
            return AnalyzeAdsResponse(
                success=False,
                ads=[],
                analysis="",
                error="No ads found for the given query"
            )
        
        analysis = await claude_service.analyze_ads(ads, request.analysis_prompt)
        
        return AnalyzeAdsResponse(
            success=True,
            ads=ads,
            analysis=analysis
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_ads: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing ads: {str(e)}"
        )
