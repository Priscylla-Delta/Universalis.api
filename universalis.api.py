import requests
import json

def main():

     # get all items ids sold on marketaboard
    marketable_Item_IDs = get_marketable_Item_IDs()
    # get all items ids and their corrosponding in game names
    ID_mappings = get_Id_mappings()

    # create a dictionary of all marketable items and their corosponding in game names
    marketable_Item_mapppings = get_marketable_Item_mapppings(marketable_Item_IDs, ID_mappings)

    # Ask the user for a valid region and item name, referencing the created dictionary to validate item names
    validated_Input = get_validated_Input(marketable_Item_mapppings)

    get_listings(validated_Input)


    return


def get_marketable_Item_IDs():

    # Get request for all items that can be sold on the mkb (Marketable items)
    marketable_Item_IDs = requests.get('https://universalis.app/api/v2/marketable', timeout=5)
    # Validate status code (200 = good)
    print("marketable_Item_IDs Status code: ",marketable_Item_IDs.status_code)
    # loads response into a list of all item id
    marketable_Item_IDs = json.loads(marketable_Item_IDs.text)
    
    ## debug structure of Item ids (Should be list)
    #print(marketable_Item_IDs)

    return marketable_Item_IDs


def get_Id_mappings():

    # Get request for all item ids with their corosponding in game names
    ID_mappings = requests.get('https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json', timeout=5)
    # Validate status code (200 = good)
    print("IDs_mapping Status code : ", ID_mappings.status_code)
    # loades response into a dictionary of all item ids and their corosponding in game names
    ID_mappings = ID_mappings.json()

    ## debug structure of Id mappings (Should be dictionary)
    #print(ID_mappings)

    return ID_mappings



def get_marketable_Item_mapppings(marketable_Item_IDs, ID_mappings):

    # intialized an empty dictionary 
    marketable_Item_mapppings = {}
    # iterates through all item ids and adds them to the dictionary along with their english name
    for Item_ID in marketable_Item_IDs:
        marketable_Item_mapppings[Item_ID] = ID_mappings[str(Item_ID)]['en']

    ## debug Structure of item mappings (Should be id : name)    
    # print(marketable_Item_mapppings)
 

    return marketable_Item_mapppings


def get_validated_Input(marketable_Item_mapppings):

    region = "North-America"
    item_id= "44177"

    validated_Input = {"region" : region,
                       "item_id" : item_id}

    return validated_Input



def get_listings(validated_Input):

    market_Data = requests.get('https://universalis.app/api/v2/North-america/2?listings=5&entries=0&statsWithin=0&fields=listings.pricePerUnit%2C+listings.worldName%2C+listings.worldID%2C+listings.quantity%2C+listings.total', timeout=5)
    print("market_Data Status code: ", market_Data.status_code)
    listings = market_Data.json()['listings']


    #print(listings[0])


    # item_index = 0
    # for listing in listings:
    #     item_index += 1
    #     print("\nitem number: ",item_index)
    #     for thing in listing:
    #         print(f"{thing}: {listing[thing]}")





    return listings





main()