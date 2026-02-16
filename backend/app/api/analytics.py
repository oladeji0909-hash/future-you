from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.api.auth import get_current_user
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/me")
async def get_my_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics for current user"""
    return AnalyticsService.get_user_analytics(current_user.id, db)

@router.get("/platform")
async def get_platform_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall platform analytics (for admin/tracking progress)"""
    # In production, add admin check here
    return AnalyticsService.get_platform_analytics(db)

@router.get("/timeline")
async def get_message_timeline(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get timeline of user's messages"""
    return AnalyticsService.get_message_timeline(current_user.id, db)

@router.get("/growth")
async def get_growth_data(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get growth chart data"""
    # In production, add admin check here
    return AnalyticsService.get_growth_chart_data(db, days)

@router.get("/retention")
async def get_retention_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user retention metrics"""
    # In production, add admin check here
    return AnalyticsService.get_retention_metrics(db)
