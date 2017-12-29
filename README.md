# urlstripscan
Strips provided link of O365 SafeLink wrapping, replaces identifying email addresses, submits to urlscan.io

## Acquire urlscan.io API Key
Details available here: https://urlscan.io/about-api/
Once key is acquired, add it to the config.ini file following the '=' sign which should be located in your working directory. 

## Install dependencies
    pip install -r requirements.txt

## Usage
urlstripscan.py [-h] [-s] link

Runs a URL through urlscan.io and provides link to report and screenshot

positional arguments:
  link        provide a link within double quotes

optional arguments:
  -h, --help  show this help message and exit
  -s, --scan  sends link to urlscan.io for analysis
  
### Example
    urlstripscan.py "http://link.here.com/login?=otherobfuscation"

The exracted URL will be outputted. If no attributable information remains, rerun same command with -s flag:

    urlstripscan.py "http://link.here.com/login?=otherobfuscation" -s


