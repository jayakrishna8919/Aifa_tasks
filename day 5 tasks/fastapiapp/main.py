#covered -> custom error handling
#        -> asynchronous code

from fastapi import FastAPI
import asyncio
import random

app = FastAPI()

class DownloadError(Exception):                             #custom exception
    def __init__(self, file_name: str, reason: str):
        self.file_name = file_name
        self.reason = reason
        super().__init__(f"Download failed for '{file_name}': {reason}")



async def download_file(file_name: str):
    print(f"Starting download for {file_name}...")
    await asyncio.sleep(random.randint(1, 3))  
    if random.random() < 0.3:
        raise DownloadError(file_name, "Connection lost.")
    print(f"Finished downloading {file_name}.")
    return {"file": file_name, "status": "success"}

@app.get("/download")
async def download_files():
    files = ["data1.csv", "data2.csv", "data3.csv", "data4.csv"]
    tasks = [download_file(f) for f in files]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    success, failures = [], []

    for r in results:
        if isinstance(r, Exception):
            if isinstance(r, DownloadError):
                failures.append({"file": r.file_name, "error": r.reason})
            else:
                failures.append({"file": "unknown", "error": str(r)})
        else:
            success.append(r)

    if failures:
        return {
            "status": "partial_failure",
            "successful": success,
            "failed": failures,
        }

    return {"status": "success", "successful": success}


@app.exception_handler(DownloadError)
async def download_error_handler(request, exc: DownloadError):
    return JSONResponse(
        status_code=500,
        content={"message": f"Custom error: {exc.file_name} - {exc.reason}"}
    )
