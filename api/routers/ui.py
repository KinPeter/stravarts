from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["ui"],
)


@router.get("/", response_class=HTMLResponse)
async def read_root():
    with open("ui/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
