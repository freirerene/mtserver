from routers import orders, prices
from utils.credentials import MT_PATH, LOGIN, PASSWORD, SERVER, API_KEY

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import MetaTrader5 as mt5

app = FastAPI(redoc_url=None, docs_url=None)


async def api_key_auth(api_key: str = Header(None, alias="x-api-key")):
    secret_api_key = API_KEY
    if api_key != secret_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )
    return api_key


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    if not mt5.initialize(MT_PATH, login=LOGIN, password=PASSWORD, server=SERVER):
        raise HTTPException(status_code=500, detail="Falha ao iniciar MetaTrader5")


@app.on_event("shutdown")
async def shutdown_event():
    mt5.shutdown()


app.include_router(orders.router)
app.include_router(prices.router)
