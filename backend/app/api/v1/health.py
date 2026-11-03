import logging
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.schemas.health import ErrorResponse, HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse, responses={503: {"model": ErrorResponse}})
def health(db: Annotated[Session, Depends(get_db)]) -> HealthResponse:
    """Check API availability and execute a real database SELECT 1."""
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.warning("Health check database query failed")
        raise HTTPException(status_code=503, detail="Database is unavailable") from None
    return HealthResponse(
        service=get_settings().app_name, version="0.1.0", timestamp=datetime.now(UTC)
    )
