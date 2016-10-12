from django.core.management.base import BaseCommand, CommandError
from app_main.models import *
from app_admin.management.utils.spider_utils import SpiderUtils
import requests
import string
import sys
from datetime import datetime
from datetime import timedelta
from datetime import date
import time
from time import mktime
from time import sleep
import csv
from bs4 import BeautifulSoup



class Command(BaseCommand):
    help = 'Runs spider for a place'

    # Can be run from command line, example usage:
    # python manage.py spider_stuff --is_debug 1
    #
    #


    def add_arguments(self, parser):

        ## allow arguments to be added
        parser.add_argument('--is_debug', nargs='+', type=int)


    def handle(self, *args, **options):

        isDebug = 0 # parameter set as 0 or 1
        try:
            isDebug = options["is_debug"][0]
        except Exception as ex:
            pass

        # utility instance
        # used by multiple spiders
        spiderUtils = SpiderUtils()

        searchUrl = "http://stuff.co.nz"
        source = "stuff.co.nz"

        searchMeArray = ["http://www.stuff.co.nz/life-style/blogs/the-omnivore",
                         "http://www.stuff.co.nz/auckland/local-news/auckland-city-harbour-news/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/nor-west-news/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/central-leader/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/eastern-courier/more_headlines"#,
                         "http://www.stuff.co.nz/auckland/local-news/east-bays-courier/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/manukau-courier/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/north-harbour-news/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/north-shore-times/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/papakura-courier/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/rodney-times/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/western-leader/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/waiheke-marketplace/more_headlines",
                         "http://www.stuff.co.nz/auckland/whats-on/food/",
                         "http://www.stuff.co.nz/auckland/local-news/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/local-blogs/tales-from-the-crypt",
                         "http://www.stuff.co.nz/auckland/local-news/local-blogs/mad-on-sport/",
                         "http://www.stuff.co.nz/auckland/local-news/reviews/photos/",
                         "http://www.stuff.co.nz/auckland/whats-on/about-town/more_headlines",
                         "http://www.stuff.co.nz/auckland/local-news/suburbanite/more_headlines"
        ]


        try:
            # logging goes through a central function
            # can add file logging at some stage
            spiderUtils.log("Started processing for " + source)
            spiderUtils.log("Options:")
            spiderUtils.log(str(options))

            # get suburb names as a single SQL request, store in memory
            # avoids running once for each request
            places = Place.objects.all()
            placeNames = [p.name for p in places]
            spiderUtils.log("Places to process: ")
            spiderUtils.log(str(placeNames))

            # clear out existing, this needs to be removed when we have duplicate checking working
            Feature.objects.all().delete
            urlArray = []

            for link in searchMeArray:
                spiderUtils.log("Requesting page: ")
                spiderUtils.log(link)
                page = requests.get(link)
                soup = BeautifulSoup(page.text, 'html.parser')
                spiderUtils.log("Soup processed")

                ## extracts a list of links for each offer
                allPosts = soup.find_all('div', attrs={'class': 'postlisting'})
                if not allPosts:
                    allPosts = soup.find_all('h2', attrs={'class': 'other_headline hot_topic'})

                for offer in allPosts:
                    data = offer.a['href']
                    data = searchUrl + data

                    ## to do: check if the article already in db
                    urlArray.append(data)

            for row in urlArray:
                self.processLink(row, places, spiderUtils)


        except Exception as ex:
            spiderUtils.log("Error: ")
            spiderUtils.log(str(ex))


    def processLink(self, urlToHit, existingPlaces, spiderUtil):

        ## extracts info from url and writes to DB

        spiderUtils = spiderUtil
        spiderUtils.log("Running for: " + urlToHit)

        category = ""
        lat = 0
        lng = 0

        page2 = requests.get(urlToHit)
        soup = BeautifulSoup(page2.text)

        fullSoup = soup.find('title')
        title = fullSoup.string
        splitPoint = title.find("|")
        title = title[:splitPoint - 1]
        title = title.strip()
        ## may need to extract special chars further:
        #title = spiderUtils.escapeSpecialHtmlChars(title)
        title = title.title()


        ## find article text
        texty = ""
        details2 = soup.findAll('p')
        for row in details2:
            ##print row
            if row.string:
                texty = texty + " " + row.string

        description = ""
        details = soup.find('meta', attrs={'property': 'og:description'})
        if details:
            description = details['content']

        ## commented text limit below
        ## this can be restricted in client/api logic
        #if len(description) > 250:
        #    description = description[:250] + "..."


        ## find article date
        dateText = soup.find('div', attrs={'class': 'toolbox_date'})
        dateText = dateText.find(text=True)  ##string
        splitPoint = dateText.find("/")
        dateText = dateText[splitPoint - 3:]
        dateText = dateText.strip()
        dateText = dateText.replace('/', ' ')
        articleDate = time.strptime(dateText, "%d %m %Y")

        dt = date.fromtimestamp(mktime(articleDate))

        ## find image
        imageLink = ""
        imageSoup = soup.find('img', attrs={'id': 'slideImg1'})
        if not imageSoup:
            imageSoup = soup.find('div', attrs={'id': 'landscapephoto'})
            if imageSoup:
                imageSoup = imageSoup.img
        if not imageSoup:
            imageSoup = soup.find('img', attrs={'class': 'photoborder'})
        if not imageSoup:
            imageSoup = soup.find('img', attrs={'style': 'float: right; margin: 5px;'})
        ##print imageSoup
        if imageSoup:
            imageLink = imageSoup['src']
            ##imageLink = imageLink.replace("..", "http://www.laurainejacobs.co.nz")
        else:
            imageLink = ""
        # to do: use imagelink ?


        ## assign category from keywords or from url title
        ## these known categories could be centralised, in utils class or database
        ## could create a "category" model
        sport_dictionary = ["cricket", "yachting", "rugby", "league", "tennis",
                            "squash", "bowls", " rowing", "archery", "badminton",
                            "baseball", "basketball", "futsal", "golf", "hockey",
                            "swimming", "triathalon", "volleyball", "waterpolo",
                            "weightlifting", "football", "water polo", "athletics",
                            "shotput", "javelin", "discus", "triple jump",
                            "long jump", "speedway", "waka ama", "dragon boat",
                            "tae kwon do", "marathon", "ironman"]


        for item in sport_dictionary:
            ## count each occurance of keyword in article
            count = texty.count(item)
            ## upper case each keyword, count again and add to total
            item = item.title()
            item = str(item)
            count2 = texty.count(item)
            count = count + count2
            if count > 2:
                category = "sports"
                ##print "category changed by keywords"

        if category == "":
            count = 0
            count2 = 0
            dining_dictionary = ["menu", "restaurant", "cooking", "flavour", "prawn",
                                 "snapper", "chicken", "duck", "poultry", "risotto", "crab",
                                 "granita", "meal", "cheese", "tart", "microgreens", "mushrooms",
                                 "fig", "cafe", "egg", "sourdough", "lobster", "eggplant", "tofu",
                                 "laksa", "curry", "tamarind", "gelato", "burger", "roti", "coriander",
                                 "scallops", "brioche", "salmon", "cannelloni", "jalapeno",
                                 "beef", "pork", "ceviche"]
            for item in dining_dictionary:
                ## count each occurance of keyword in article
                count = texty.count(item)
                ## upper case each keyword, count again and add to total
                item = item.title()
                item = str(item)
                count2 = texty.count(item)
                count = count + count2
                if count > 6:
                    category = "dining"
                    ##print "category changed by keywords"

        if "blogs/the-omnivore" in urlToHit or "life-style/food-wine" in urlToHit or "whats-on/food" in urlToHit or "local-news/reviews/food" in urlToHit:
            category = "dining"
        if "local-blogs/mad-on-sport" in urlToHit:
            category = "sports"
            ##print "category changed by url"

        if category == "":
            category = "news"

        ## check if suburb is in the text anywhere by reading in
        ## post text then iterate thru looking for suburb name
        ## check the suburb & assign subid
        ## read in suburb data

        for suburb in existingPlaces:
            if suburb.name in texty:

                spiderUtils.log("Loading for place: " + suburb.name)
                spiderUtils.log("Creating feature: " + title)
                # create feature, an abstracted table row
                # avoids using SQL directly
                feature = Feature()
                feature.description1 = title
                feature.description2 = description
                feature.link = urlToHit
                feature.company = "stuff.co.nz"
                feature.place = suburb
                if dt:
                    feature.date_feature = dt
                feature.category = category
                spiderUtils.log("Saving feature")
                # saves feature to database
                feature.save()
                spiderUtils.log("Saved: " + str(feature.id))


