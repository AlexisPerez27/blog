from celery import shared_task

import logging 
import redis

from .models import PostAnalytics, Post
from django.conf import settings



logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

@shared_task 
def increment_post_impression(post_id):
    # logger.info("Update post impresion")
    # INCREMENTA LOS POST ASICIADOS 
    try: 
        analytics,created = PostAnalytics.objects.get_or_create(post__id=post_id)
        analytics.increment_impression()
    except Exception as e:
        logger.info(f"Error al incrementar impression para el ID {post_id}: {str(e)}")



@shared_task 
def sync_impression_db():
    #sincronisar las impresiones almacenadas con redis con la base de datos

    keys = redis_client.keys("post:impression:*")

    for key in keys:
        try: 
            post_id = key.decode("utf-8").split(":")[-1]

            impressions = int(redis_client.get(key))

            analytics,created = PostAnalytics.objects.get_or_create(post__id=post_id)
            # analytics.impressions += impressions
            analytics.increment_impression()
            analytics.save()

            analytics._update_click_through_rate()


            redis_client.delete(key)

        except Exception as e:
            print(f"Error en sincronizacion impression para el ID {key}: {str(e)}")



@shared_task
def increment_post_views_task(slug, ip_add):
    try: 
        post = Post.objects.get(slug=slug)
        post_analytics = PostAnalytics.objects.get_or_create(post=post)
        post_analytics.increment_view(ip_add)
    except Exception as e:
        print(f"Error al incrementar las vistas {slug}: {str(e)}")