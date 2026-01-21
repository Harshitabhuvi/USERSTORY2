import logging

logging.basicConfig(          # SETS :Log level,TimestampMessage ,format
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s" 
)

logger = logging.getLogger(__name__)   #Creates a logger per module.
