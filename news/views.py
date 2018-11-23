import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView, ArchiveIndexView

from .models import News
from .scraper import samakal
from .scraper import priyo
from .scraper import palo
from .scraper import kalerkonto
from .scraper import chanel_i
from .scraper import bdnews24


def scrape_news(request):
    samakal("http://samakal.com/list/all")
    priyo("https://www.priyo.com/")
    palo("https://www.prothomalo.com/home/featured")
    kalerkonto("http://www.kalerkantho.com/")
    chanel_i("https://www.channelionline.com/%E0%A6%B8%E0%A6%B0%E0%A7%8D%E0%A6%AC%E0%A6%B6%E0%A7%87%E0%A6%B7/")
    bdnews24("https://bangla.bdnews24.com/")
    return redirect(reverse('news-list'))


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = News.objects.all()
        start_date = datetime.date.today()
        day = self.kwargs.get('days')
        if day:
            day = int(day)
            if day == 1:
                queryset = News.objects.filter(added__date=start_date)
            else:
                end_date = start_date - datetime.timedelta(day)
                queryset = News.objects.filter(added__range=(end_date, start_date))
        return queryset


class NewsYearArchiveView(YearArchiveView):
    queryset = News.objects.all()
    date_field = "added"
    make_object_list = True
    allow_future = True


class NewsMonthArchiveView(MonthArchiveView):
    queryset = News.objects.all()
    date_field = "added"
    allow_future = True


class NewsDayArchiveView(DayArchiveView):
    queryset = News.objects.all()
    date_field = "added"
    allow_future = True
    month_format = '%m'
    context_object_name = 'news'
    template_name = 'news/news_list.html'


class NewsSearch(View):

    def post(self, request):
        search_text = request.POST.get('search')
        if search_text:
            results = News.objects.filter(title__icontains=search_text).distinct()
        else:
            results = ['No Items found']
        return render(request, 'news/ajax_search.html', {'results': results})
