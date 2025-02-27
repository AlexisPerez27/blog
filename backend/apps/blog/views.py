from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework_api.views import StandardAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException
import redis
from django.conf import settings

from .models import Post, Heading, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer, PostView
from .utils import get_client_ip
from .task import increment_post_impression, sync_impression_db,increment_post_views_task
from core.permissions import HasValidAPIKeY
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)


""" class PostListView(ListAPIView):
    queryset = Post.postobject.all()
    serializer_class = PostListSerializer """


class PostListView(StandardAPIView):
    permission_classes = [HasValidAPIKeY]

    def get(self, request,*args, **kwargs):

        try: 

            cached_posts = cache.get("post_list")

            if cached_posts: 
                for post in  cached_posts: 
                    increment_post_impression.delay(post['id'])
                    # redis_client.incr(f"post:impressions:{post['id']}") #NO ME FUNCIONO 
                return self.paginate_response_with_extra(request,cached_posts, extra_data="extra_data aqui")

            posts = Post.postobject.all()

            if not posts.exists():
                raise NotFound(detail="No se encontro resultado")
            
            serialized_posts = PostSerializer(posts, many= True).data

            for post in  posts: 
                increment_post_impression.delay(post.id)
                # redis_client.incr(f"post:impressions:{post.id}") #NO ME FUNCIONO 

            cache.set("post_list", serialized_posts, timeout=60 * 5)

        except Post.DoesNotExist:
            raise NotFound(detail="No se encontro el resultado del post ")
        except Exception as e:
            raise APIException(detail=f"Un error a ocurrido {str(e)}")

        return self.paginate_response_with_extra(request,serialized_posts, extra_data="extra_data aqui")



""" class PostDetails(RetrieveAPIView):
    queryset = Post.postobject.all()
    serializer_class = PostSerializer
    lookup_field = 'slug' """



class PostDetails(StandardAPIView):
    permission_classes = [HasValidAPIKeY]
    
    # @method_decorator(cache_page(60 * 1))
    def get(self, request):
        ip_add = get_client_ip(request)

        slug = request.query_params.get("slug")
        try:

            cached_post = cache.get(f"post_detail:{slug}")

            if cached_post: 
                
                increment_post_views_task.delay(cached_post['slug'], ip_add)
                return self.response(cached_post)

            posts = Post.postobject.get(slug=slug)
            serialized_posts = PostSerializer(posts).data

            cache.set(f"post_detail:{slug}", serialized_posts, timeout=60 * 5)
        except Post.DoesNotExist:
            raise NotFound(detail="La solicitud no existe")
        except Exception as e:
            raise APIException(detail=f"Un error a ocurrido {str(e)}")

        

        # posts.views +=1
        # posts.save()

        # client_ip = get_client_ip(request)

        # if PostView.objects.filter(post=posts, ip_address=client_ip).exists():
        #     return Response(serialized_posts)
        


        # PostView.objects.create(post=posts, ip_address=client_ip)

        """ try:

            post_analytics = PostAnalytics.objects.get(post=posts)
            post_analytics.increment_view(request)
        except PostAnalytics.DoesNotExist:
            raise NotFound(detail="La solicitud no existe")
        except Exception as e:
            raise APIException(detail=f"Un error a ocurrido mientras se intento actualizar los analisis {str(e)}") """

        return self.response(serialized_posts)




class PostHeadingView(StandardAPIView):
    permission_classes = [HasValidAPIKeY]
    def get(self,request):
        post_slug = request.query_params.get("slug")
        heading_object = Heading.objects.filter(post__slug = post_slug)
        serialized_data = HeadingSerializer(heading_object, many=True).data
        return self.response(serialized_data)
    """ serializer_class = HeadingSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter(post__slug = post_slug) """
    


class IncrementPostClicView(APIView):
    permission_classes = [HasValidAPIKeY]
    def post(self,request,slug):
        """se incrementa el contador de clicks dependiendo de su slug"""
        try:
            posts = Post.postobject.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="La solicitud no existe")
        

        try: 
            post_analytics, created = PostAnalytics.objects.get_or_create(post=posts)
            post_analytics.increment_click()    
        except Exception as e:
            raise APIException(detail=f"Un error a ocurrido mientras se intento actualizar los analisis {str(e)}")

        return Response({
            "message": "Click incremented satisfactorio",
            "clicks": post_analytics.clicks
        })



#video de python tiempo 4:26:52
# https://www.youtube.com/watch?v=btkK5IAuDDA&ab_channel=SoloPython

# ver el video tambien
# https://www.youtube.com/watch?v=uSbDMs7Y9yI&ab_channel=UskoKruM2010