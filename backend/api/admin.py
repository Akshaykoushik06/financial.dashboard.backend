from django.contrib import admin
from .models import Todo, HomePageModel

# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed')


class HomePageAdmin(admin.ModelAdmin):
    list_display = ('foodCardBalance',)


admin.site.register(Todo, TodoAdmin)
admin.site.register(HomePageModel, HomePageAdmin)
