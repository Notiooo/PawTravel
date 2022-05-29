from django.conf import settings
import importlib


LIKES_OBJS_DICT = getattr(settings, 'LIKES_OBJS_DICT', {})

LIKES_OBJS = [getattr(importlib.import_module(i), j) \
              for i in LIKES_OBJS_DICT \
              for j in LIKES_OBJS_DICT[i]
              ]
