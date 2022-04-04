from celery.utils.log import get_task_logger
from config import celery_app
from PIL import Image

from.models import File


logger = get_task_logger(__name__)

@celery_app.task(name="generate_thumbnail")
def generate_thumbnail(file_name, file_id, file_type):
    """generate a thumbnail for img file and save it to db"""
    if 'image' in file_type:
        output = f'thumbnails/{file_name}'
        img = Image.open(f"{file_name}")
        img.thumbnail((128,128), Image.ANTIALIAS)
        img.save(output)

        file = File.objects.get(id=file_id)
        file.thumbnail = output.replace('/uploads', '')
        file.save()

        logger.info(f"Thumbnail generated for file: {file_name}")
        return output

    logger.info(f"Thumbnail only works for img file.")
    return