import sys
import json
from pprint import pprint
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import seaborn as sns
from matplotlib import *
sns.set(color_codes=True)


# read the entire file into a python array
with open('yelp_dataset/yelp_academic_dataset_review.json', 'rb') as f:
    rev_data = f.readlines()

# remove the trailing "\n" from each line
rev_data = map(lambda x: x.rstrip(), rev_data)

# each element of 'data' is an individual JSON object.
# i want to convert it into an *array* of JSON objects
# which, in and of itself, is one large JSON object
# basically... add square brackets to the beginning
# and end, and have all the individual business JSON objects
# separated by a comma
rev_data_length = len(rev_data)
rev_data_length_decile = rev_data_length//10
# rev_data_length_decile = rev_data_length//100
coffee_shops = pd.read_pickle("coffee_shops.pkl")
reviews_list = []
# for i in range(0,10):
for i in range(0,2):
    rev_data_json_str = "[" + ','.join(rev_data[i*rev_data_length_decile:(i+1)*rev_data_length_decile]) + "]"

    # # now, load it into pandas

    rev_data_df = pd.read_json(rev_data_json_str)

    # print(rev_data.head())
    # if i == 0:
    #     reviews = rev_data_df[rev_data_df.business_id.isin(coffee_shops.business_id)]
    # else:
    #     review_temp = rev_data_df[rev_data_df.business_id.isin(coffee_shops.business_id)]
    #     reviews.append(review_temp)
    reviews = rev_data_df[rev_data_df.business_id.isin(coffee_shops.business_id)]
    reviews_list.append(reviews)

reviews = pd.concat(reviews_list)
word_list = []
for index, items in enumerate(reviews.text):
    items = items.lower()
    items = items.split()
    for word in items:
        word = word.replace("?","")
        word = word.replace(".","")
        word = word.replace("!","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace(";","")
        word = word.replace('"',"")
        word = word.replace("'","")
        word = word.replace("\n","")
    word_list = word_list + items




stop_words = set(stopwords.words('english'))
list_of_words = []
word_list_length = len(word_list)
i_count = 0

# for doc in word_list:
#     list_of_words = [i for i in doc if i not in stop_words] + list_of_words
#     i_count = i_count + 1
#     print(word_list_length - i_count)

counted_words = Counter(word_list)
stop_words.update(['place', "it's",'like','good','get','great','really','one','also',"i'm",'go','would',
    "i've",'always','time',"don't",'little','nice','love','back','even','-','best','staff','never','come','shop',
    'know','coffee.','much','make','got','friendly','could','want','think','cup','coffee,','going','ordered','way','try',
    'well','every','around','right','definitely','&',"can't",'drink','it.',"didn't",'pittsburgh','menu','work',
    'storm','order','since','first',"you're",'next','need','see','better',"that's",'sure','still','something','ever',
    'find','location','selection','drinks','two','lot','many','here.','bit','day','favorite','made','take','came',
    'hot','feel','free','last','went','good.','stop','new','usually','place.'])


for sword in stop_words:
    del counted_words[sword]


counted_words_df = pd.DataFrame.from_dict(counted_words, orient = 'index', dtype='int32')
counted_words_df.reset_index(inplace=True)

counted_words_df.columns = ['Words', 'Count']
counted_words_df.sort(columns=['Count'], ascending=[False], inplace = True)
# plot_count = counted_words_df.Count.iloc[0:20]
# plot_words = counted_words_df.Word.iloc[0:20]
plot_data = counted_words_df.iloc[0:20]
x_labels = plot_data.Words.values

sns.set_style("whitegrid")
# counted_words_data = sns.load_dataset("plot_data")
ax = sns.barplot(x="Words", y="Count", data=plot_data)
ax.set_xticklabels(x_labels, rotation=45, fontsize=16)
sns.set_context("notebook", font_scale=2)
# ax.set_xticklabels(labels, rotation=45)

sns.plt.show()
