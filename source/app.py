from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Request,
    HTTPException
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse
)

from fastapi.staticfiles import StaticFiles

from fastapi.templating import (
    Jinja2Templates
)

from source.config import (
    STATIC_DIR,
    TEMPLATES_DIR
)

from source.schema import (
    QueryRequest,
    QueryResponse,
    HealthResponse,
    AgentInfoResponse
)

from source.database_queries import (
    validate_database_connection
)

from source.rag_pipeline import (
    get_retriever
)

from source.agent import (
    run_agent,
    get_agent_info
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    if not validate_database_connection():

        raise RuntimeError(
            "Database validation failed."
        )

    get_retriever()

    yield


app = FastAPI(
    title="Financial Analyst Agent",
    version="1.0.0",
    lifespan=lifespan
)


templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


from fastapi.responses import HTMLResponse

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get(
    "/health",
    response_model=HealthResponse
)
async def health():

    return {
        "status": "healthy"
    }


@app.get(
    "/agent_info",
    response_model=AgentInfoResponse
)
async def agent_info():

    return get_agent_info()


@app.post(
    "/main/chat",
    response_model=QueryResponse
)
async def chat(
    request: QueryRequest
):

    try:

        response = run_agent(
            request.query
        )

        return QueryResponse(
            status="success",
            response=response
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc)
        }
    )