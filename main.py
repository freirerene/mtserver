import MetaTrader5 as mt5
from fastapi import FastAPI, HTTPException

from routers import orders, prices

app = FastAPI(redoc_url=None, docs_url=None)


@app.on_event("startup")
async def startup_event():
    if not mt5.initialize():
        raise HTTPException(
            status_code=500, detail=f"Falha ao iniciar MetaTrader5 {mt5.last_error()}"
        )


@app.on_event("shutdown")
async def shutdown_event():
    mt5.shutdown()


app.include_router(orders.router)
app.include_router(prices.router)
