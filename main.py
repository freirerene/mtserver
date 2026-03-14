import MetaTrader5 as mt5
from fastapi import FastAPI

from routers import orders, prices
from utils.credentials import LOGIN, MT_PATH, PASSWORD, SERVER

app = FastAPI(redoc_url=None, docs_url=None)


@app.on_event("startup")
async def startup_event():
    kwargs = {}
    if MT_PATH:
        kwargs["path"] = MT_PATH
    if LOGIN:
        kwargs["login"] = int(LOGIN)
    if PASSWORD:
        kwargs["password"] = PASSWORD
    if SERVER:
        kwargs["server"] = SERVER

    if not mt5.initialize(**kwargs):
        raise RuntimeError(
            f"Falha ao iniciar MetaTrader5: {mt5.last_error()}"
        )


@app.on_event("shutdown")
async def shutdown_event():
    mt5.shutdown()


app.include_router(orders.router)
app.include_router(prices.router)
