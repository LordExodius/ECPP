# i just want a goddamn alex drawer please for the love of god
# july 20th 2021
# oscar yu

import urllib.request
import json
import os
from table import table

caStores = {
    "149" : "North York",
    "372" : "Vaughan",
    "256" : "Etobicoke",
    "040" : "Burlington",
    "004" : "Ottawa",
    "039" : "Montreal",
    "414" : "Boucherville",
    "559" : "Quebec City",
    "529" : "Halifax",
    "249" : "Winnepeg",
    "349" : "Edmonton",
    "216" : "Calgary",
    "313" : "Coquitlam",
    "003" : "Richmond"
}

def stockTrack(item : str, country = "ca", location = None) -> None:
    item = item.replace(".", "")
    url = f"https://api.ingka.ikea.com/cia/availabilities/ru/{country}?itemNos={item}&expand=StoresList,Restocks,SalesLocations"
    headers = {
        "authority": "api.ingka.ikea.com",
        "method": "GET",
        "path": f"/cia/availabilities/ru/{country}?itemNos={item}&expand=StoresList,Restocks,SalesLocations",
        "scheme": "https",
        "accept": "application/json;version=2",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.ikea.com",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-client-id": "b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631"
    }

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = json.loads(response.read().decode("utf-8"))

    #dataTable = [["Store", "StoreID", "Quantity", "Restock", "Early Restock", "Late Restock"]]
    dataTable = [["Store", "StoreID", "Quantity", "Online", "Restock", "Early Restock", "Late Restock"]]
    rowNum = 0

    location = location.replace(" ", "").replace("+", "").split(",")
    
    availabilities = data["availabilities"]
    for store in availabilities:
        #TABLE
        storeInfo = []
        rowNum += 1

        # Identify store
        storeCode = store["classUnitKey"]["classUnitCode"]

        # If store location is specified, only scan data for that store location
        if location[0] != "" and not storeCode in location:
            print("BREAK")
            continue

        if storeCode in caStores:
            storeName = caStores[storeCode]

            carrying = store["buyingOption"]["cashCarry"]

            if not "availability" in carrying:
                continue

            # Identify current availability
            availStats = carrying["availability"]
            quantAvail = availStats["quantity"]
            availOnline = store["availableForClickCollect"]

            #TABLE
            storeInfo.append(storeName)
            storeInfo.append(storeCode)
            storeInfo.append(quantAvail)
            storeInfo.append(availOnline)

            # Identify restock quantity and dates if restock data exists
            if "restocks" in availStats:
                restock = availStats["restocks"][0]
                quantRestock = restock["quantity"]
                restockEarly = restock["earliestDate"]
                restockLate = restock["latestDate"]

                #TABLE
                storeInfo.append(quantRestock)
                storeInfo.append(restockEarly)
                storeInfo.append(restockLate)
            
            #TABLE
            else:
                storeInfo.append("N/A")
                storeInfo.append("N/A")
                storeInfo.append("N/A")
            
            #TABLE
            dataTable.append(storeInfo)

        # Unknown store
        else:
            pass

    storeTable = table(dataTable)
    #print(storeTable)

    html = f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>~oscar</title><link rel="icon" href="../res/awwThumbs.svg" sizes="any" type="image/svg+xml"/><link rel="stylesheet" href="../../styles.css"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet"></head><body><div id="main"><header><h1>ikea</h1><h2><a href="../index.html">../</a></h2><p>IKEA stock tracking tool.</p><p>Local download with alerts coming soon™.</p></header><div id="content"><pre class="mono">'
    html += str(storeTable)
    html += '</pre></div></div></body>'
    print(html)

stockTrack(os.environ["sku"], os.environ["cCode"] , os.environ["storeID"])