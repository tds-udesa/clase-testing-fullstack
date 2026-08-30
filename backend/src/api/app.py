from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.dogs import router as dogs_router
from src.api.schemas.problem_details import ProblemDetails
from src.config.settings import get_settings
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    servers=[
        {
            "url": "http://localhost:8000/api/v1",
            "description": "Local development server",
        }
    ],
    title="Dogs API - Clase Testing",
    version="0.1.0",
    contact={"name": "Alejo Villores", "email": "avillores@udesa.edu.ar"},
    root_path="/api/v1",
    root_path_in_servers=False,
)

origins = get_settings().cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ProblemDetails(
            type="https://example.com/http-exception",
            title="HTTP Exception",
            status=exc.status_code,
            detail=str(exc.detail),
            instance=str(request.url),
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ProblemDetails(
            type="https://example.com/validation-error",
            title="Validation Error",
            status=422,
            detail=exc.__dict__,
            instance=str(request.url),
        ).model_dump(),
    )


app.include_router(dogs_router, prefix="/dogs", tags=["dogs"])
