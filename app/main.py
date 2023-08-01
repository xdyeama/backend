from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.trips.router import router as trips_router
from app.news.router import router as news_router

from app.config import client, env, fastapi_config
from .jobs.jobs import scheduler

app = FastAPI(**fastapi_config)


scheduler.start()


@app.on_event("shutdown")
def shutdown_db_client():
    client.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=env.CORS_ORIGINS,
    allow_methods=env.CORS_METHODS,
    allow_headers=env.CORS_HEADERS,
    allow_credentials=True,
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(trips_router, prefix="/trips", tags=["Trips"])
app.include_router(news_router, prefix="/news", tags=["News"])
