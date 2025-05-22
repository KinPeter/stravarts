import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
