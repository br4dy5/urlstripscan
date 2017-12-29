# urlstripscan
This script will take a URL, including one encoded by O365 SafeLinks and Base64, strip out attributable email addresses, 
run it through urlscan.io, and provide links to analysis & screenshot. This will allow for analysis without attribution.

## Acquire urlscan.io API Key
Details available here: https://urlscan.io/about-api/
Once key is acquired, add it to the config.ini file following the '=' sign which should be located in your working directory. 

## Install dependencies
    pip install -r requirements.txt

## Usage
urlstripscan.py [-h] [-s] link

positional arguments:

link        provide a link within double quotes

optional arguments:

-h, --help  show this help message and exit

-s, --scan  sends link to urlscan.io for analysis
  
### Example
    urlstripscan.py "http://link.here.com/login?=otherobfuscation"

The exracted URL will be outputted. If no attributable information remains, rerun same command with -s flag:

    urlstripscan.py "http://link.here.com/login?=otherobfuscation" -s


