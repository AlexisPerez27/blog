from rest_framework import serializers

from .models import Post, Categoria, Heading, PostView

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
        """ fields = [
            'id',
            'parent',
            'nombre',
            'titulo',
            'descripcion',
            'imagenes',
            'slug',
        ] """

class CategoriaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'nombre',
            'slug',
        ]


class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = [
            "titulo",
            "slug",
            "level",
            "order",
        ]


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    headings = HeadingSerializer(many=True)
    # views = PostViewSerializer(many=True)
    view_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = "__all__"

    def get_view_count(self, obj):
        return obj.postview.count()

class PostListSerializer(serializers.ModelSerializer):
    categoria = CategoriaListSerializer()    
    headings = HeadingSerializer(many=True)
    views = PostViewSerializer(many=True)
    view_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "id",
            "titulo",
            "descripcion",
            "imagenes",
            "slug",
            "created_at",
            "updated_at",
            "categoria",
            "headings",
            "views",
            "view_count"
        ]
    def get_view_count(self, obj):
        return obj.postview.count()






# tiempo video 3:01:49
# https://www.youtube.com/watch?v=btkK5IAuDDA&ab_channel=Fazt


# tambien ver este otro video django con bootstrap
# https://www.youtube.com/watch?v=uSbDMs7Y9yI&ab_channel=UskoKruM2010