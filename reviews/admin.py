from django.contrib import admin
from .models import App, ReviewsContent, SplitWords

# Register your models here.


class AppAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'app_name', 'have_data',
                    'app_category', 'date_time')


class ReviewsContentAdmin(admin.ModelAdmin):
    list_display = ('review_app_id_id', 'review_title',
                    'review_rating', 'review_split', 'review_content')


admin.site.register(App, AppAdmin)
admin.site.register(ReviewsContent, ReviewsContentAdmin)
admin.site.register(SplitWords)
