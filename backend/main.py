from typing import Optional
from fastapi import Depends, FastAPI, Query, Request, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader, HTTPBearer
from jobs.visibility_job import run_visibility_job
from middleware.rate_limit import register_rate_limiter
from middleware.auth import APIKeyMiddleware
from enums.time_visibility import TimeVisibility
from enums.site_visibility import SiteVisibility
from enums.search_order import SearchOrder
from dependencies import create_site_service, get_site_service
from services.site_service import SiteService
from fastapi.staticfiles import StaticFiles
from schemas.site import Site
from schemas.site_summary import SiteSummary
import os
from config import settings
from contextlib import asynccontextmanager
from jobs.scheduler import start_scheduler

swagger_api_key = APIKeyHeader(name="x-api-key", auto_error=False)

def _should_skip_visibility_job() -> bool:
    val = os.environ.get("SKIP_VISIBILITY_JOB", "").strip().lower()
    return val in ("1", "true", "yes")

@asynccontextmanager
async def lifespan(app: FastAPI):
    site_service = create_site_service()
    app.state.site_service = site_service
    start_scheduler(app)
    if not _should_skip_visibility_job():
        await run_visibility_job(site_service)
    yield

app = FastAPI(
    lifespan=lifespan,
    dependencies=[Security(swagger_api_key)]
)

api_primary_key = settings.Secrets.Key
app.add_middleware(APIKeyMiddleware, api_key=api_primary_key)
register_rate_limiter(app)

# CORS settings
origins = [
    "https://thestarchaser.com",
    "http://localhost:8081",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve light pollution tiles
tiles_dir = os.path.join(os.path.dirname(__file__), "image_tiles")
app.mount("/tiles", StaticFiles(directory=tiles_dir), name="tiles")

@app.get("/sites", response_model=list[SiteSummary])
async def get_sites(site_service: SiteService = Depends(get_site_service)) -> list[SiteSummary]:
    return await site_service.get_all_sites()

@app.get("/site/{site_id}", response_model=Site)
async def get_site(
    site_id: int,
    time: Optional[TimeVisibility] = Query(
        TimeVisibility.TONIGHT,
        description="Time window used to evaluate site visibility. Note: TimeVisibility.NOW is currently unimplemented and defaults to tonight. (job does not precompute it)."
    ),
    site_service: SiteService = Depends(get_site_service),
) -> Site:
    return await site_service.get_site(site_id, time)

@app.get(
        "/sites/search", 
        response_model=list[Site],
        summary="Search observation sites",
        description=(
            "Search sites by name and/or proximity.\n\n"
            "- `lat`, `lon`, `drive_time`: required - return sites within drive time of location\n"
            "- `name`: optional substring match on site name\n"
            "- `limit`, `offset`: pagination; `order_by`: Distance or Visibility"
        ))
async def search(
    lat: float = Query(..., description="Latitude (required)"),
    lon: float = Query(..., description="Longitude (required)"),
    drive_time: int = Query(..., description="Drive time to site in minutes (required)"),
    name: Optional[str] = None,
    visib: Optional[SiteVisibility] = Query(
        SiteVisibility.Terrible,
        description="Overall site visibility rating",
    ),
    time: Optional[TimeVisibility] = Query(
        TimeVisibility.TONIGHT,
        description="Time window used to evaluate site visibility. Note: TimeVisibility.NOW is currently unimplemented (job does not precompute it)."
    ),
    limit: int = Query(25, ge=1, le=500, description="Max results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    order_by: SearchOrder = Query(SearchOrder.Visibility, description="Primary sort: Distance or Visibility"),
    site_service: SiteService = Depends(get_site_service),
) -> list[Site]:
    return await site_service.search(
        visib=visib,
        time=time,
        lat=lat,
        lon=lon,
        drive_time=drive_time,
        name=name,
        limit=limit,
        offset=offset,
        order_by=order_by,
    )

@app.post("/jobs/visibility/run")
async def run_visibility_job_now(site_service: SiteService = Depends(get_site_service)):
    await site_service.precompute_visibility([
        TimeVisibility.TONIGHT,
        TimeVisibility.TOMORROW_NIGHT,
        TimeVisibility.NIGHTS_3_FROM_NOW,
    ])
    return {"status": "ok"}