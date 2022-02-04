from celery.utils.log import get_task_logger
from config import celery_app

logger = get_task_logger(__name__)

@celery_app.task(name="generate_thumbnail")
def generate_thumbnail(file_id):
    """generate a thumbnail for img file"""
    logger.info(f"Thumbnail generated for file id: {file_id}")
    print('eff')
    return 'DONE'