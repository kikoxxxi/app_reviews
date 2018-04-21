import json
import random
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from reviews.models import App, ReviewsContent, SplitWords

# Create your views here.


def home(request):
    template = get_template('index.html')
    app_list = App.objects.all()
    html = template.render(locals())
    return HttpResponse(html)


def bubble(request, id):
    try:
        app = App.objects.get(app_id=str(id))
    except App.DoesNotExist:
        raise Http404

    # 获取各评分的数量
    rating_dict = {}
    review = ReviewsContent.objects.filter(review_app_id_id=str(app.id))
    for record in review:
        if rating_dict.get(record.review_rating, None):
            rating_dict[record.review_rating] += 1
        else:
            rating_dict[record.review_rating] = 1

    # 获取各版本的各评分的数量
    # 先获取所有版本
    # 再计算各版本的各评分

    # 获取关键词频率
    word_dict = {}
    split = SplitWords.objects.filter(word_app_id_id=str(app.id))
    with open('static/countwords.csv', 'w', encoding='utf-8') as f:
        for record in split:
            if word_dict.get(record.word, None):
                word_dict[record.word] += 1
            else:
                word_dict[record.word] = 1
        word_list = sorted(word_dict.items(),
                           key=lambda asd: asd[1], reverse=True)  # 按频率降序
        f.write("id,value\n")
        f.write("f,\n")
        count = 4
        end = 0
        for i in range(count):
            f.write("f.{},\n".format(i))
            gap = random.randint(8, 20)
            start = end
            end = start + gap
            for item in word_list[start:end]:
                f.write("f.{}.{},{}\n".format(i, item[0], str(item[1])))
        f.write("f.{}.{},{}".format(
            count - 1, word_list[end][0], str(word_list[end][1])))
    template = get_template('bubble.html')
    html = template.render(locals())
    return HttpResponse(html)
