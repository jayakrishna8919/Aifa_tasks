# app/core/logger.py
import logging

logging.basicConfig(filename="newfile.log",filemode ='w+')
logger = logging.getLogger("fastapi_project")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(" %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
print(ch)
