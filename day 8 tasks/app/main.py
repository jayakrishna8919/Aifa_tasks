from fastapi import FastAPI,Request
from routers.routes import router
import uuid
import time
import logging


logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("request-logger")




app = FastAPI()
@app.middleware("http")
async def custom_logging_middleware(request: Request, call_next):
    # Generating unique request ID
    request_id = str(uuid.uuid4())
    
   
    method = request.method
    url = str(request.url)
    client_ip = request.client.host

    logger.info(f" [{request_id}] Incoming Request: {method} {url} from {client_ip}")

    start_time = time.time()

    response = await call_next(request)

    process_time = round(time.time() - start_time, 4)

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)

  
    logger.info(
        f" [{request_id}] Response: {response.status_code} "
        f"({process_time}s)"
    )

    return response

@app.get("/hello")
async def hello():
    return {"message": "Hello World!"}

app.include_router(router)






