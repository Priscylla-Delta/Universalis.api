import requests
import json
import sys

def main():

     # get all items ids sold on marketaboard
    marketable_Item_IDs = get_marketable_Item_IDs()
    # get all items ids and their corrosponding in game names
    ID_Mappings = get_Id_Mappings()

    # create a dictionary of all marketable items and their corosponding in game names
    marketable_Item_Mapppings = get_marketable_Item_Mapppings(marketable_Item_IDs, ID_Mappings)

    # Ask the user for a valid region and item name, referencing the created dictionary to validate item names
    validated_Input = get_validated_Input(marketable_Item_Mapppings)

    # create a dictionary of all the listings for the given item and region
    listings = get_listings(validated_Input)

    #use the listings and make a purchase order for the user
    purchase_Order= get_purchase_Order(listings, validated_Input['quantity'])

    return


def get_marketable_Item_IDs():

    # Get request for all items that can be sold on the mkb (Marketable items)
    marketable_Item_IDs = requests.get('https://universalis.app/api/v2/marketable', timeout=5)
    # Validate status code (200 = good)
    print("marketable_Item_IDs Status code: ",marketable_Item_IDs.status_code)
    # loads response into a list of all item id
    marketable_Item_IDs = json.loads(marketable_Item_IDs.text)
    
    # # debug structure of Item ids (Should be list)
    #print(marketable_Item_IDs)

    return marketable_Item_IDs


def get_Id_Mappings():

    # Get request for all item ids with their corosponding in game names
    ID_Mappings = requests.get('https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/master/libs/data/src/lib/json/items.json', timeout=5)
    # Validate status code (200 = good)
    print("IDs_mapping Status code : ", ID_Mappings.status_code)
    # loades response into a dictionary of all item ids and their corosponding in game names
    ID_Mappings = ID_Mappings.json()    

    # # debug structure of Id mappings (Should be dictionary)
    #print(ID_Mappings)

    return ID_Mappings



def get_marketable_Item_Mapppings(marketable_Item_IDs, ID_Mappings):

    # intialized an empty dictionary 
    marketable_Item_Mapppings = {}
    # iterates through all item ids and adds them to the dictionary along with their english name
    for Item_ID in marketable_Item_IDs:
        marketable_Item_Mapppings[Item_ID] = ID_Mappings[str(Item_ID)]

    # # debug Structure of item mappings (Should be id : name)    
    # print(marketable_Item_Mapppings)
 
    return marketable_Item_Mapppings


def get_validated_Input(marketable_Item_Mapppings):

    # input("region: ")
    # input("item name: ")

    region = "North-America"
    item_id= "44162"
    language = "en"
    quantity = 500

    validated_Input = {"region" : region,
                       "item_ID" : item_id,
                       "language" : language,
                       "quantity" : quantity}

    return validated_Input


def get_listings(validated_Input):

    # Grabs relevent url data from the user input
    region = validated_Input["region"]
    item_ID = validated_Input["item_ID"]
    # Constructs a valid url with the givin inputs
    market_data_url = "https://universalis.app/api/v2/" + region + "/" + item_ID + "?entries=0&statsWithin=0&fields=listings.pricePerUnit%2C+listings.worldName%2C+listings.quantity%2C+listings.total%2C+listings.listingID"
    
    # Get request for all the relevent market data for the given item and region (PricePerUnit, Quantity, WorldName, WorldID, ListingID, Total)
    market_Data = requests.get(market_data_url, timeout=5)
    # Validate status code (200 = good)
    print("market_Data Status code: ", market_Data.status_code)
    # loads response into a list of dictionaries for each listing and their fields
    listings = market_Data.json()['listings']
    
    # # debug Structure of listings (should be list of dictionaries with all their respective fields)
    # print(listings)
    

    # Make a dictionary of listings organized by their listingID
    # Initializes and empty Dictionary
    listing_IDs_Dict = {}

    # Iterates through each listing, intializing an empty dict with name equal to the listing ID
    for listing in listings:
        listing_IDs_Dict[listing['listingID']] = {}
        
        # Iterates through each field of the listing and copies them over to the new dictionary organized by id
        for field in listing:
            listing_IDs_Dict[listing['listingID']][field] = listing[field]
        
    # # Debugg for Validating Dictionary integrity         
    # print(listing_IDs_Dict)
    
    return listing_IDs_Dict


def get_purchase_Order(listings, quantity):
    
    # Initialize a purchase order to store the list of listing Id's
    purchase_order = []

    while quantity > 0:

        # If there are no listings (should be checked elsewhere but alas)
        if len(listings) == 0:
            return purchase_order

        # Iterate through a copy of each listing's id and grab the quantity being sold
        for listing in list(listings):
            listing_quantity = listings[listing]['quantity']
            
            # If the listing quanitity is less or equal to the quantity being baught, subtract that amount
            # and add the listing id to the purchase order and remove the listingID from the listings Dict
            # such that the incrimentation backup doesnt reuse listings 
            if listing_quantity <= quantity:
                quantity = quantity - listing_quantity
                purchase_order.append(listing)
                listings.pop(listing, None)
                

            if quantity == 0:
                # If youve bought exactly enough, stop the loop
                # # Debugg for validating Purchase order structure, should be a list of Listing Ids
                print(purchase_order)
                return purchase_order
            
        quantity += 1





# def make_change(input, coins):
#     used_Coins = []
#     i = 0
#     while input > 0:
#         if coins[i] <= input:
#             input = round(input - (coins[i]), ndigits=2)
#             used_Coins.append(coins[i])

#         else:
#             i += 1

#     return used_Coins


main()