from typing import Optional

from pydantic import BaseModel


class GetHistory(BaseModel):
    symbol: str
    timeframe: str
    check_hour: Optional[bool] = True
    ticks: Optional[int] = 0
    from_date: Optional[str] = ""


class TradeRequest(BaseModel):
    symbol: str
    volume: float
    deviation: int
    magic: Optional[int] = 100
    comment: Optional[str] = "FastAPI order"
