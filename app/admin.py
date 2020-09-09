from django.contrib import admin
from .models import BoardModel,Comment,Reply

admin.site.register(BoardModel)
admin.site.register(Comment)
admin.site.register(Reply)
