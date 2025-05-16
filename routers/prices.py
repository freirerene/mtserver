import re
import time
from datetime import datetime

from fastapi import APIRouter

from utils.mtfunctions import get_history, get_ticks
from utils.schemas import GetHistory

router = APIRouter()


@router.get("/tick/{symbol}")
async def tick_endpoint(symbol: str):
    tick_info = get_ticks(symbol)
    return tick_info


@router.post("/history")
async def history_endpoint(info_request: GetHistory):

    df = get_history(info_request)
    if info_request.check_hour:
        df = check_if_current(df, info_request)

    return df.to_dict(orient="records")


def check_if_current(df, info_request):
    timeframe = info_request.timeframe
    current_hour = what_to_check(timeframe)
    if not current_hour:
        return df

    timeframe = re.search(r"\D", timeframe)[0]
    dots = ""
    while current_hour != int(df["time"].dt.strftime(f"%{timeframe}").iloc[-1]):
        dots += "."
        print(f"\r{dots}", end="")
        df = get_history(info_request)
        time.sleep(1)

    return df


def what_to_check(timeframe):

    if (timeframe == "H1") or (timeframe == "H4"):
        return datetime.today().hour
    elif (
        (timeframe == "M1")
        or (timeframe == "M5")
        or (timeframe == "M15")
        or (timeframe == "M30")
    ):
        return datetime.today().minute
    else:
        return
