from django.contrib import admin

from .models import Categoria, Post, Heading, PostAnalytics

@admin.register(Categoria)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("parent","nombre","titulo","slug")
    search_fields = ("nombre","titulo", "descripcion, slug")
    prepopulated_fields = {'slug': ('nombre',)}
    list_filter=('parent',)
    ordering = ('nombre',)
    readonly_fields = ("id",)
    list_editable = ("titulo",)


class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1
    fields = ('titulo','level','order','slug')
    prepopulated_fields = {'slug': ('titulo',)}
    ordering = ('order',)

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo","status","categoria","created_at","updated_at")
    search_fields = ("titulo","descripcion","contenido","keywords","slug")
    prepopulated_fields = {'slug': ('titulo',)}
    list_filter=('status','categoria','updated_at',)
    ordering = ('-created_at',)
    readonly_fields = ("id","created_at","updated_at")
    fieldsets = (
        ('Informacion General',{
            'fields' : ('titulo','descripcion','contenido','imagenes','keywords','slug', 'categoria')
        }),
        ('Fechas & estatus',{
            'fields': ('status','created_at','updated_at')
        })
    )

    inlines = [HeadingInline]

# @admin.register(Heading)

# class HeadingAdmin(admin.ModelAdmin):
#     list_display = ('titulo','post','level','order')
#     search_fields = ('titulo', 'post__titulo')
#     list_filter = ('level','post')
#     ordering = ('post','order')
#     prepopulated_fields = {'slug': ('titulo',)}




@admin.register(PostAnalytics)
class PostAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('post_title','views','impressions','clicks','click_through_rate','avg_time_on_page',)
    search_fields = ('post__title',)
    readonly_fields = (
        'post_title',
        'post',
        'views',
        'impressions',
        'clicks',
        'click_through_rate',
        'avg_time_on_page',
    )
    
    def post_title(self,obj):
        return obj.post.titulo
    
    post_title.short_description = 'Post Title'