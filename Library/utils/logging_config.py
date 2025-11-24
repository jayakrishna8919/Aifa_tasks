import logging


logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            filename="lms.log"
        )

logger = logging.getLogger("lms")
logger.info("Logging initialized")
        
