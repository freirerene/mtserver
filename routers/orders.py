from utils.schemas import TradeRequest
from utils.mtfunctions import buy, sell, close

from fastapi import APIRouter

router = APIRouter()


@router.post("/buy")
async def buy_order(trade: TradeRequest):
    buy_info = buy(trade)
    return buy_info


@router.post("/sell")
async def sell_order(trade: TradeRequest):
    sell_info = sell(trade)
    return sell_info


@router.get("/close-all")
async def close_all_positions():
    close_info = close()
    return close_info
