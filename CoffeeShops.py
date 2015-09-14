import sys
import json
from pprint import pprint
import pandas as pd
from collections import Counter

# review_file = open("yelp_dataset/yelp_academic_dataset_review.json")
# business_file = open("yelp_dataset/yelp_academic_dataset_business.json")
# business_file = pd.read_csv("yelp_dataset/yelp_academic_dataset_business.csv",dtype={'attributes.Ambience.divey':pd.np.bool})

# business_list = []

# for line in business_file:
#     business_list.append(json.loads(line))

# print business_list[0]

# business = pd.read_json(business_list)

# read the entire file into a python array
with open('yelp_dataset/yelp_academic_dataset_business.json', 'rb') as f:
    biz_data = f.readlines()

# remove the trailing "\n" from each line
biz_data = map(lambda x: x.rstrip(), biz_data)

# each element of 'data' is an individual JSON object.
# i want to convert it into an *array* of JSON objects
# which, in and of itself, is one large JSON object
# basically... add square brackets to the beginning
# and end, and have all the individual business JSON objects
# separated by a comma
biz_data_json_str = "[" + ','.join(biz_data) + "]"

# now, load it into pandas
biz_data = pd.read_json(biz_data_json_str)

# nan_drop = biz_data.dropna(subset = ['categories'])

# print biz_data.describe()
# print nan_drop.describe()

# print biz_data.categories



def StringContains(category_list):
    if any('Coffee' in s for s in category_list) or any('Cafes' in s for s in category_list):
        return True
    else:
        return False

# print(biz_data.head())

coffee_shops = biz_data[biz_data['categories'].map(StringContains)]
# coffee_shops = biz_data[biz_data['categories'].str.contains('coffee')]
# print(biz_data.describe(),coffee_shops.describe())

# print(Counter(coffee_shops))


coffee_shops = coffee_shops[['business_id','categories','city','name','neighborhoods','state','stars','review_count']]

print(coffee_shops.head())

coffee_shops.to_pickle("coffee_shops.pkl")

