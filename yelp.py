# prototype yelp scraper, Bennur S 2015

import urllib2
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import itertools
import time
from time import mktime
from datetime import datetime

def thanN(ratings,N):
    # return filter based on ratings
    # if N=4, return filter of all >=4
    # if N=-4, return filter of all <=4
    thanN = []
    if N>0:
        for num in ratings:
            if num>=N:
                thanN.append(True)
            else:
                thanN.append(False)
    elif N<0:
        for num in ratings:
            if num<=N:
                thanN.append(True)
            else:
                thanN.append(False)
    return thanN
    
def filteredReviews(reviews,filt):
    RevF = itertools.compress(reviews,rPos)
    Revs = [rev for rev in RevF]
    return Revs
    
def revS(reviews):
    alltext = []
    # convert to usable strings
    for review in reviews:
        alltext.extend(review.strings)
    # convert it all into a long string
    alltextString = ''.join(alltext)
    # clean up
    alltextString.lower()
    alltextString.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return alltextString

def scrapeYelp(bizname):
    thereismore = True
    baseurl = 'http://www.yelp.com/biz/'
    bizurl = baseurl+bizname
    rn = 0 # #reviews scraped
    reviews = []
    ratings = []
    datepub = []
    while thereismore:
        tryurl = bizurl+'?start='+str(rn)
        response = urllib2.urlopen(tryurl)
        html = response.read()
        # parse with BeautifulSoup
        parsedHtml = BeautifulSoup(html)
        # check to see if there are more reviews
        if not parsedHtml.find_all(itemprop="description"):
            print 'Finished for now'
            thereismore = False
        else: 
            print 'Scraped '+ str(rn) + ' reviews'
            # Find review text
            reviews.extend(parsedHtml.find_all(itemprop="description"))
            # Find ratings
            ratings.extend(parsedHtml.find_all(itemprop="ratingValue")[1:])
            # find date of published review
            datepub.extend(parsedHtml.find_all(itemprop="datePublished"))
            rn += 40 # next 40 reviews
    return ratings, reviews, datepub

def ratingsToN(ratings):
    ratingF = []
    # convert to numbers
    for line in ratings:
        # lline['content'] to access the content of the bs4.element.tag object
        ratingF.append(float(line['content']))
    return ratingF
    
def dpTodt(dates):
    dateN = [] 
    for date in dates:
        dateT = date['content']
        dateTT = time.strptime(dateT, "%Y-%m-%d")
        dateN.append(datetime.fromtimestamp(mktime(dateTT)))
    return dateN
    
def showandsave(text,background,name):
    # wordcloud for positive reviews
    wc = WordCloud(background_color=background, stopwords=stopwords,
                        width=1800, height=1400).generate(text)
    wc.to_file(name)
    # Open a plot of the generated image.
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

# First get all the information
bizname = 'honest-toms-taco-shop-philadelphia'
ratings, reviews, datepub = scrapeYelp(bizname)
print len(ratings)
print len(reviews)
print len(datepub)

# then process it
ratingsN = ratingsToN(ratings)
alltext = revS(reviews)
dates = dpTodt(datepub)

# Wordcloud additions
stopwords = STOPWORDS.copy()
stopwords.add("honest")
stopwords.add("Tom's")

# Generate the wordcloud for all reviews
# vars: background_color="white", max_words=2000, mask=alice_coloring,
# stopwords=STOPWORDS.add("said"), max_font_size=40, random_state=42
# stopwords=STOPWORDS, background_color='black', width=1800, height=1400
wc = WordCloud(background_color="white", stopwords=stopwords,
                    width=1800, height=1400).generate(alltext)
# Open a plot of the generated image.
plt.imshow(wc)
plt.axis("off")
plt.show()
wc.to_file(bizname+"-allRevs.png")

rPos = thanN(ratingsN,4)
rNeg = thanN(ratingsN,-2)
# rNeg = [not i for i in rPos]
posText = revS(filteredReviews(reviews,rPos))
negText = revS(filteredReviews(reviews,rNeg))

showandsave(posText,"green",bizname+"-posRevs.png")
showandsave(negText,"red",bizname+"-negRevs.png")
