from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.post import router as post_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.vote import router as vote_router


# * as we use alembic, the following line is no longer needed.
# Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)
