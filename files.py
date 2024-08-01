import os
import time
import requests
from notion_client import Client
from pprint import pprint

def main():
    mdPath = {FILE_LOCATION}
    validFiles = []

    for name in os.listdir(mdPath):
        if name.endswith("md"):
            validFiles.append(name)

    app = True
    banner()
    while(app):
        res = menu()
        if(res == 0):
            printFileContents(validFiles, mdPath)
        elif(res == 1):
            syncToNotion(validFiles, mdPath)
        elif(res == 2):
            fileInformation(validFiles, mdPath)
        elif(res == 3):
            app = False
        
#Start menu, controls program complexity
def menu():
    print("\nControl Menu")
    print("------------------")
    options = ["print files", "sync to notion", "file information", "exit"]
    for x in range(len(options)):
        print("[" + str(x) + "]: " + options[x])
    myNum = input("Option number: ")
    return int(myNum)

def printFileContents(validFiles, mdPath):
    for f in validFiles: 
        print("\n--------    " + f + "    --------\n")
        print((open(mdPath + r"\\" + f, "r")).read())
        print("\n--------    " + "End of File" + "    --------\n\n\n")

#Get the information of the current file
def fileInformation(validFiles, mdPath):
    print("\nFiles & Information\n")
    numFiles = 0
    for f in validFiles:
        numFiles+=1
        currFileLines = (open(mdPath + r"\\" + f, "r")).readlines()
        currCount = 0
        for line in currFileLines:
            currCount+=1
        print(f + " - Number of Lines: " + str(currCount))
    print("\nThere are " + str(numFiles) + " markdown files")

#Syncing function
def syncToNotion(validFiles, mdPath):
    notion = Client(auth={SECRET})
    list_users_response = notion.users.list()
    #pprint(list_users_response)
    syncing = True
    print("\nsyncing", end = "")
    runInfo = {'New File': 0, 'Updated': 0}
    while(syncing):
        print(".", end = "")
        time.sleep(1)
        database_id = list_users_response["results"][0]["id"]
        #Loop through current files to update
        for index in range(len(validFiles)):
            if(checkDatabase(validFiles, mdPath, notion, index) == 0):
                runInfo.update({'New File': runInfo["New File"] + 1})
                newPage = {
                    "File": {"title": [{"text": {"content": validFiles[index]}}]
                    },
                }
                child =  [
                    {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{ "type": "text", "text": { "content": (open(mdPath + r"\\" + validFiles[index], "r")).read()  } }]
                    }
                    }
                ]
                notion.pages.create(parent={"database_id":{DB_ID}}, properties=newPage, children=child)   
                print(".", end = "")
        syncing = False  
    print("\nsyncing complete.")
    runDetails(runInfo)

#Check the given database whether the file already exists
def checkDatabase(validFiles, mdPath, notion, index):
    my_page = notion.databases.query(
    **{
        "database_id": {DB_ID},
        "filter": {
            "property": "File",
            "rich_text": {
                "contains": validFiles[index],
            },
        },
    }
    )
    return(len(my_page["results"]))

def runDetails(details):
    print("Run Details:")
    print(str(details['New File']) + " Files Created")
    print(str(details['Updated']) + " Files Updated")



def banner():
    font = '''
   ******              **           **      **     **        
  **////**            /**          /**     /**    /** ****** 
 **    //   ******   ******  ***** /**     /**    /**/**///**
/**        //////** ///**/  **///**/****** /**    /**/**  /**
/**         *******   /**  /**  // /**///**/**    /**/****** 
//**    ** **////**   /**  /**   **/**  /**/**    /**/**///  
 //****** //********  //** //***** /**  /**//******* /**     
  //////   ////////    //   /////  //   //  ///////  //      '''
    print(font)

main()
