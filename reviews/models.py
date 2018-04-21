from django.db import models

# Create your models here.


class App(models.Model):
    app_id = models.CharField(max_length=15)
    app_name = models.CharField(max_length=50)
    have_data = models.CharField(max_length=2)
    app_category = models.CharField(max_length=50, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{},{}".format(self.app_id, self.app_name)

    class Meta:
        ordering = ['-date_time']
        unique_together = ['app_id', 'app_name']


class ReviewsContent(models.Model):
    review_app_id = models.ForeignKey(App, on_delete=models.CASCADE)
    review_content = models.TextField(null=True, blank=True)
    review_version = models.CharField(max_length=20)
    review_rating = models.CharField(max_length=2)
    review_title = models.TextField(null=True, blank=True)
    review_split = models.CharField(max_length=2)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{},{}".format(self.review_app_id, self.review_content)

    class Meta:
        ordering = ['-date_time']


class SplitWords(models.Model):
    word_app_id = models.ForeignKey(App, on_delete=models.CASCADE)
    word = models.CharField(max_length=20)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{},{}".format(self.word_app_id, self.word)

    class Meta:
        ordering = ['-date_time']
