import requests
import json

def main():

     # get all items ids sold on marketaboard
    marketable_Item_IDs = get_marketable_Item_IDs()
    # get all items ids and their corrosponding in game names
    ID_Mappings = get_Id_Mappings()

    # create a dictionary of all marketable items and their corosponding in game names
    marketable_Item_Mapppings = get_marketable_Item_Mapppings(marketable_Item_IDs, ID_Mappings)

    # Ask the user for a valid region and item name, referencing the created dictionary to validate item names
    validated_Input = get_validated_Input(marketable_Item_Mapppings)

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


def get_Id_Mappings():

    # Get request for all item ids with their corosponding in game names
    ID_Mappings = requests.get('https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json', timeout=5)
    # Validate status code (200 = good)
    print("IDs_mapping Status code : ", ID_Mappings.status_code)
    # loades response into a dictionary of all item ids and their corosponding in game names
    ID_Mappings = ID_Mappings.json()    

    ## debug structure of Id mappings (Should be dictionary)
    #print(ID_mappings)

    return ID_Mappings



def get_marketable_Item_Mapppings(marketable_Item_IDs, ID_Mappings):

    # intialized an empty dictionary 
    marketable_Item_Mapppings = {}
    # iterates through all item ids and adds them to the dictionary along with their english name
    for Item_ID in marketable_Item_IDs:
        marketable_Item_Mapppings[Item_ID] = ID_Mappings[str(Item_ID)]

    ## debug Structure of item mappings (Should be id : name)    
    # print(marketable_Item_Mapppings)
 

    return marketable_Item_Mapppings


def get_validated_Input(marketable_Item_Mapppings):

    # input("region: ")
    # input("item name: ")

    region = "North-America"
    item_id= "44177"
    language = "en"
    quantity = "100"

    validated_Input = {"region" : region,
                       "item_ID" : item_id,
                       "language" : language,
                       "quantity" : quantity}

    return validated_Input



def get_listings(validated_Input):

    region = validated_Input["region"]
    item_ID = validated_Input["item_ID"]

    #temporary listing amount (to be deleted for actual use)
    listings_amount = "listings=5&"

    market_data_url = "https://universalis.app/api/v2/" + region + "/" + item_ID + "?" + listings_amount + "entries=0&statsWithin=0&fields=listings.pricePerUnit%2C+listings.worldName%2C+listings.worldID%2C+listings.quantity%2C+listings.total"
   
    ##debugg
    # print(market_data_url)

    market_Data = requests.get(market_data_url, timeout=5)
    print("market_Data Status code: ", market_Data.status_code)
    listings = market_Data.json()['listings']
    

    item_index = 0
    for listing in listings:
        item_index += 1
        print("\nitem number: ",item_index)
        for thing in listing:
            print(f"{thing}: {listing[thing]}")





    return listings





main()