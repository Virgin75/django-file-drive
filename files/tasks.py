from celery.utils.log import get_task_logger
from config import celery_app
from PIL import Image


logger = get_task_logger(__name__)

@celery_app.task(name="generate_thumbnail")
def generate_thumbnail(file_name):
    """generate a thumbnail for img file"""
    output = f'thumbnails/{file_name}'
    img = Image.open(f"{file_name}")
    img.thumbnail((128,128), Image.ANTIALIAS)
    img.save(output)

    logger.info(f"Thumbnail generated for file: {file_name}")
    return output