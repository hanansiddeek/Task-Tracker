from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from database.connection import connect_db
from routes.tasks import tasks_api
from utils.logger import setup_logger
from routes import tasks
from custom_exceptions import NonExistentTaskError, InvalidDataError, DatabaseConnectionError
import logging


@tasks_api.on_event("startup")
async def startup_event():
    connect = connect_db()
    print(connect)


# Create FastAPI application
tasks_api: FastAPI = FastAPI()
tasks_api.include_router(tasks.tasks_api)

# Set up the logger
logger = logging.getLogger(__name__)
setup_logger(logger, log_file_path='C:\\Users\\Hanan Siddeeek\\Desktop\\Task\\app.log')


# Exception handler for RequestValidationError
@tasks_api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )


# Exception handler for HTTPException
@tasks_api.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Custom exception handler for specific cases
@tasks_api.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, NonExistentTaskError):
        logger.error(f"Non-existent task error: {exc}")
        return JSONResponse(status_code=404, content={"detail": "Task not found"})
    elif isinstance(exc, InvalidDataError):
        logger.error(f"Invalid data error: {exc}")
        return JSONResponse(status_code=400, content={"detail": "Invalid data"})
    elif isinstance(exc, DatabaseConnectionError):
        logger.error(f"Database connection error: {exc}")
        return JSONResponse(status_code=500, content={"detail": "Database connection error"})
    else:
        logger.error(f"An unexpected error occurred: {exc}")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# Middleware to log requests
@tasks_api.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    return response
