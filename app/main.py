"""FastAPI application entry point."""

from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

from app.common.config import API_PORT, FASTAPI_CONFIG
from app.routes.aws_services_routes import router

app = FastAPI(*FASTAPI_CONFIG


@app.get("/", include_in_schema=False)
def root():
    """Redirects the root URL to the API documentation.

    This endpoint is not included in the OpenAPI schema, serving only as
    a convenience for users to quickly access the documentation.
    """

    return RedirectResponse(url="/docs")


api_router = APIRouter()
api_router.include_router(router, tags=["aws_s3"])
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=API_PORT, reload=True)
