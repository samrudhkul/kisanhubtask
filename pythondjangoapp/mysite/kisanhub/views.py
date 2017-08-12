from django.http import HttpResponse
import urllib.request
from bs4 import BeautifulSoup
import re
from .models import Weatherdata
from graphos.sources.model import ModelDataSource
from graphos.renderers.yui import BarChart
from django.shortcuts import render

# Create your views here.
def index(request):

   country=["UK ","England ","Wales ","Scotland "]
   weather_typ=[" Tmax"," Tmin"," Tmean"," Sunshine"," Rainfall"]
   Weatherdata.objects.all().delete()
   for cnt in country:
     for wtype in weather_typ:
      site=urllib.request.Request('http://www.metoffice.gov.uk/climate/uk/summaries/datasets#Yearorder',headers={'User-Agent': 'Mozilla/5.0'})
      url=urllib.request.urlopen(site).read()
      soup = BeautifulSoup(url, 'html.parser')

      link= soup.find_all('a',title=re.compile("{}Date{}".format(cnt,wtype)))
      print(link)
      req = urllib.request.Request(link[0]["href"],headers={'User-Agent': 'Mozilla/5.0'})
      temp=urllib.request.urlopen(req)

      listtext=list(temp.readlines())

      print(type(listtext))

      m_or_s=listtext[7:][0].decode().split()[1:]

      for i in range(len(listtext)-8):
        k=-1
        for j in listtext[8:][i].decode().split():
          if listtext[8:][i].decode().split().index(j)!=0:
            k=k+1
            try:
               reading=float(j)

            except:
               reading=0
            w=Weatherdata(weather_type=wtype,weather_country=cnt,weather_year=year,month_or_season=m_or_s[k],weather_reading=reading,unique_string=cnt+str(year)+wtype+m_or_s[k])
            w.save()
            print(reading,year,m_or_s[k],cnt,wtype)

          else:
           year=int(j)

   return HttpResponse("Hello, world. You're at the kisanhub index.")

def weatherchart(request):
    queryset = Weatherdata.objects.filter(month_or_season="JAN",weather_country="UK ",weather_type=" Rainfall")
    data_source = ModelDataSource(queryset, fields=[
            'weather_year', 'weather_reading'])
    chart = BarChart(data_source)
    return render(request,template_name='kisanhub/weatherchart.html',context={'chart': chart})