import logging
import os
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger("stores."+__name__)


def get_env(key, default_value=None):
    try:
        return os.environ[key]
    except KeyError:
        if default_value is None:
            raise ImproperlyConfigured(
                f"{key} is not part of environment variables, please add !"
            )
        return default_value


def create_thumbnails(pk, model, size_set, image_attr=None):
    from versatileimagefield.image_warmer import VersatileImageFieldWarmer

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