# AMR MONITORING CONFIGURATION TOOLBOX
## Overview
This program is intended to function as a webscraper with the purpose of trackinng antimicrobial resistance related data in India, using Google and ChatGPT. With this being said, the configurable nature of the text files and json files allows this program to be used in several other contexts.
## PyPI and pip
This program is configured for Python on Windows. Below are the modules it makes use of and, with them, the pip commands required to install them.
- python-dotenv, pip install python-dotenv
- - Used to read the .env file.
- Selenium, pip install selenium
- - Used as the browser-accessing tool.
- Webdriver Manager, pip install webdriver-manager
- - Used in conjunction with Selenium to access the internet, provides the browser.
- OpenAI, pip install openai
- - Used to communicate with ChatGPT.

To install these automatically, just run the file "install_required_modules.bat". If you would prefer to do this manually, just copy the commands seen above into a command prompt console.

## Configuring files
### .env 
If you want this to work semi-seamlessly, the first thing that must be done is the creation 
of a file named ".env". This file must be placed in the same folder that all the python files are located. 
This file must have the following line in it:

OPENAI_API_KEY='whatever your api key is, keep the inverted commas'

This will allow the OpenAI api to function.
### config.json
This file allows you to change the behaviour of the program. It is presented in the following format/s:

- self explanatory text variable name : "bunch of text",
- self explanatory numerical variable name : integer,
- self explanatory boolean variable name : false/true,
- self explanatory array variable name : [
    "text",
    number,
    "whatever is fitting just separate using commas"
]

Do not change the name of the variable but feel free to change the value or modify / contribute to the contents of the array it is assigned to.
## Configuring folders
### api_commands 
#### example_requests.txt
_coming soon to a script near you (when implemented / important)_
TL;DR for editing purposes:
This is meant to be an example request for one shot learning, basically an example input followed by what would be an ideal output from chatgpt.
#### request.txt
This text file contains the text used as the main prompt given to ChatGPT. The scripts function by checking the initial response for a "Yes." or "No." and then proceeding to extract the relevant data from the message if it exists. The relevant metrics aiming to be extracted from the article are prompted in place of the "\<v>" and they are extracted from the file in the same folder "variables_to_extract.txt".

Lines 1 - 2 can be modified.
#### synopsis.txt
This text file contains the text used as a filtering prompt given to ChatGPT. The purpose of this is to determine whether or not the full article is "worth" being passed to ChatGPT if the description given on the front page of Google is not relevant in the slightest.

Lines 1 - 3 can be modified. In "config.json", the variable "check synopsis before passing full article" forces the script to do a synopsis check or not - if it is set to a value of "false" (without the quotation marks) then this text won't be used and the opposite will happen for "true".
#### variables_to_track.txt
This text file contains the variables ChatGPT is prompted to extract from the websites as well as pieces of text that provide either formatting information or additional context, in brackets.

You can modify the entire file. It is recommended that the variables being extracted and their associated terms in brackets remain simple to discourage strange responses from ChatGPT. **If you wish to change this after having run the program, it is recommended that you move the previously produced csv files to another folder so as to not produce errors and lose data due to the presence of new headings.**

### query_generation
#### _keywords.txt
The title of this section refers to any file with the suffix "_keywords.txt". These files are intended to have variables names pertaining to the names of the files.

You can add or remove files with this naming convention so long as the the variables present in the file "templates.txt" follow the convention seen below:
- filename    :   variable in the sentence of templates
- whatever_the_file_is_named_keywords.txt : <whatever_the_file_is_named>

#### templates.txt
This file contains themplate search queries intended to be filled with variables designated as keywords. The convention described through bullet points above applies to this file as well.

You can add or remove lines in this file as long as they abide by the convention.
### outputs
This folder houses the outputs - one continuous csv file to keep track of all data and one csv file that gets overwritten each time the program is run for ease of separating the two.

These files, except for their headings, can be altered.
### website_data 
This folder contains two files, "blacklist.txt" and "urls.txt". "blacklist.txt" operates such that any piece of text on the page, if seen in the url of an article, will cause the url to not be investigated further. "urls.txt" exists to track the urls of webpages that have been visited and are not to be visited again to save on computational power and API credits.

Both files can be altered.
