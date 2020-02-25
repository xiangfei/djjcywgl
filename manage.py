#!/usr/bin/env python
import os
import sys
if __name__ == "__main__":
    environment =  os.environ.get('DJANGO_ENV')
    if environment == 'production':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jcywgl.settings_production")

    elif environment == 'test':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jcywgl.settings_test")

    elif environment == 'preview':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jcywgl.settings_preview")
        
    elif environment == 'develop':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jcywgl.settings_develop")

    else:
        import logging
        logger  = logging.getLogger()
        logger.warning('not find  DJANGO_ENV use default env, please set if necessary')
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jcywgl.settings_local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

