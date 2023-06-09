from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import os
from routers import outfits
from queries.authenticator import authenticator
from routers import accounts, ratings

app = FastAPI()

# origins = [
#         'http://localhost:3000',
#         os.environ.get("CORS_HOST", None),
#         'https://fitcheck.one',
#         'https://lads51.gitlab.io',
#         'https://www.fitcheck.one',
#         "https://lads51.gitlab.io/module3-project-gamma",
#         "https://fitcheck-api.dec-ct-3.mod3projects.com",
# ]


@app.get("/", tags=["Landing Page"])
async def root():
    return {"message": "Welcome to FitCheck API!"}


app.include_router(outfits.router, tags=["Outfits"])
app.include_router(authenticator.router, tags=["Authentication"])
app.include_router(accounts.router, tags=["Accounts"])
app.include_router(ratings.router, tags=["Ratings"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://fitcheck.one'],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"],
    allow_headers=["*"],
    expose_headers=["pragma"],
    max_age=315576000
)
