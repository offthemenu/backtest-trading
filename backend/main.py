from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import data_loader, backtest

app = FastAPI()

# CORS middleware (ok to leave * during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(data_loader.router)
app.include_router(backtest.router)
