import logging

from celery import shared_task
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

logger = logging.getLogger(__name__)

# todo run on celery


def create_thumbnails(pk, model, size_set, image_attr=None):
    instance = model.objects.get(pk=pk)

    if not image_attr:
        image_attr = "image"

    image_instance = getattr(instance, image_attr)
    if image_instance.name == "":
        return
    warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance, rendition_key_set=size_set, image_attr=image_attr
    )

    logger.info("Creating thumbnails for  %s", pk)
    num_created, failed_to_create = warmer.warm()
    if num_created:
        logger.info("Created %d thumbnails", num_created)
    if failed_to_create:
        logger.error("Failed to generate thumbnails", extra={"paths": failed_to_create})