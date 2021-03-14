from django.contrib import admin
from .models import Post
from .models import QueryForm
from .models import *

# Register your models here.
admin.site.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','Name_of_service_provider','title','text','Price','Contact_number','created_date','published_date']

admin.site.register(QueryForm)

class QuestionAdmin(admin.ModelAdmin):
    list_display=('title','user')
    search_fields=('title','detail')
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)

class CommentAdmin(admin.ModelAdmin):
    list_display=('answer','comment')
admin.site.register(Comment,CommentAdmin)

class UpvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')
admin.site.register(UpVote,UpvoteAdmin)

class DownvoteAdmin(admin.ModelAdmin):
    list_display=('answer','user')
admin.site.register(DownVote,DownvoteAdmin)
