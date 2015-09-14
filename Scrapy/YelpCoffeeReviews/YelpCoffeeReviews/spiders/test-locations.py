import pickle

# location_strings = pickle.load( open( "saved_locations.p", "rb" ) )

# start_urls = []
# for location in location_strings:
#     start_urls.append("http://www.yelp.com/search?start=0&cflt=coffee&l=p:" + location)




# print(len(location_strings))
# if 'NY:New_York:Manhattan:' in location_strings: location_strings.remove('NY:New_York:Manhattan:')
# if 'NY:New_York::' in location_strings: location_strings.remove('NY:New_York::')

# # pickle.dump( location_strings, open( "saved_locations.p", "wb" ) )

test_string  = '\n            Showing 1-10 of 42574\n        '
sampe = test_string.split()
print(sampe[-1])
