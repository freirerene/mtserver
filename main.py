import os

import MetaTrader5 as mt5
from fastapi import FastAPI

from routers import orders, prices

app = FastAPI(redoc_url=None, docs_url=None)


def _build_mt5_kwargs():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    kwargs = {}
    mt_path = os.getenv("MT_PATH")
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    server = os.getenv("SERVER")

    if mt_path:
        kwargs["path"] = mt_path
    if login:
        kwargs["login"] = int(login)
    if password:
        kwargs["password"] = password
    if server:
        kwargs["server"] = server

    return kwargs


@app.on_event("startup")
async def startup_event():
    kwargs = _build_mt5_kwargs()

    if not mt5.initialize(**kwargs):
        raise RuntimeError(
            f"Falha ao iniciar MetaTrader5: {mt5.last_error()}"
        )


@app.on_event("shutdown")
async def shutdown_event():
    mt5.shutdown()


app.include_router(orders.router)
app.include_router(prices.router)
