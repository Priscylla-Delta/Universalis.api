import requests
import json



marketable_Items_IDs = requests.get('https://universalis.app/api/v2/marketable', timeout=5)
marketable_Items_IDs = json.loads(marketable_Items_IDs.text)

market_Data = requests.get('https://universalis.app/api/v2/North-america/2?listings=5&entries=0&statsWithin=0&fields=listings.pricePerUnit%2C+listings.worldName%2C+listings.worldID%2C+listings.quantity%2C+listings.total', timeout=5)
listings = market_Data.json()['listings']

IDs_mapping = requests.get('https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json', timeout=5)
IDs_mapping = IDs_mapping.json()

#print(IDs_mapping['1']['en'])


# for marketable_Item_ID in marketable_Items_IDs:
#     print(IDs_mapping[marketable_Item_ID]['en'])

for marketable_Item_ID in marketable_Items_IDs:
    print(IDs_mapping[str(marketable_Item_ID)]['en'])




# for id in IDs_mapping:
#     print(IDs_mapping[id]['en'])



#print(marketable_Items_IDs)



#print(data.text[])

#listings = json.loads(listings.text)


#print(listings[0])


# item_index = 0
# for listing in listings:
#     item_index += 1
#     print("\nitem number: ",item_index)
#     for thing in listing:
#         print(f"{thing}: {listing[thing]}")

#print(data['Listings'])






#for key,value in listings['listings']:
    #print(f"{key}: {value}")