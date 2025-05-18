from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
import asyncio
import json
import os
from typing import AsyncGenerator
from kaggle.api.kaggle_api_extended import KaggleApi

app = FastAPI()

os.environ['KAGGLE_USERNAME'] = 'your_kaggle_username'
os.environ['KAGGLE_KEY'] = 'your_kaggle_api_key'

api = KaggleApi()
api.authenticate()

async def get_kaggle_datasets(search_term="climate", page=1, page_size=5) -> list:
    """
    Use Kaggle API to fetch paginated datasets.
    """
    datasets = api.dataset_list(search=search_term, sort_by="hottest", page=page, page_size=page_size)
    return [d.__dict__ for d in datasets]

async def kaggle_data_stream(search_term="climate", page=1, page_size=5) -> AsyncGenerator[str, None]:
    """
    SSE generator for paginated Kaggle datasets.
    """
    yield "retry: 10000\n\n"
    try:
        datasets = await get_kaggle_datasets(search_term, page, page_size)
        for data in datasets:
            await asyncio.sleep(0.5)
            yield f"data: {json.dumps(data)}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.get("/stream")
async def stream_kaggle_data(
    request: Request,
    search: str = Query("climate"),
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=100)
):
    """
    SSE endpoint with pagination and search term.
    """
    return StreamingResponse(
        kaggle_data_stream(search_term=search, page=page, page_size=page_size),
        media_type="text/event-stream"
    )

@app.get("/download")
async def download_dataset(dataset: str = Query(..., description="Dataset ref like 'zynicide/wine-reviews'")):
    """
    Download a Kaggle dataset by its reference.
    """
    try:
        download_path = os.path.join("downloads", dataset.replace("/", "_"))
        os.makedirs(download_path, exist_ok=True)
        api.dataset_download_files(dataset, path=download_path, unzip=True)
        
        zip_path = download_path + ".zip"
        if os.path.exists(zip_path):
            return FileResponse(path=zip_path, filename=f"{dataset.replace('/', '_')}.zip", media_type='application/zip')
        else:
            return {"message": "Dataset downloaded and extracted in folder", "path": download_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
