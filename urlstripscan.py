#! python3

'''
This script will take a URL, including one encoded by SafeLinks/Base64, strip out attributable email addresses, 
run it through urlscan.io, and provide links to analysis. This will allow for analysis without attribution.
'''


import requests
import time
import argparse
import urllib.parse
import re
import configparser


config = configparser.ConfigParser()
config.read("config.ini")
api_key = config.get("scanio", "api_key")


def parse():
    '''
    Parses link provided as command line argument in double quotes
    '''
    parser = argparse.ArgumentParser(description='Runs a URL through urlscan.io and provides link to report and screenshot')
    parser.add_argument("link", help='provide a link within double quotes')
    parser.add_argument('-s', '--scan', action="store_true", default=False, help='sends link to urlscan.io for analysis')
    args = parser.parse_args()

    global link
    link = args.link
    global needs_analysis
    needs_analysis = args.scan


def decode(parsed):
    '''
    Decode URL
    Replace username, password attributes and remove returns/new lines
    '''
    decoded = urllib.parse.unquote(parsed).replace("\r","").replace("\n","")
    return decoded


def strip(decoded):
    '''
    Strips the O365 SafeLink and html wrapping.
    '''
    stripped = decoded.replace("https://na01.safelinks.protection.outlook.com/?url=", "")
    stripped = stripped.partition("&amp;data=")[0]
    stripped = stripped.partition("&data=")[0]
    return stripped


def redact(stripped):
    '''
    Redacts/replaces email addresses to a non-attributable address
    '''
    p = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    redacted = p.sub('username@domain.com', stripped)
    return redacted


def base64(redacted):
    '''
    Identifies base64 encoding string and replaces with base64 encoded string: username@domain.com
    '''

    p2 = re.compile(r"[a-zA-Z0-9]+==")
    raw_link = p2.sub('dXNlcm5hbWVAZG9tYWluLmNvbQ==', redacted)
    return raw_link


def extract(base64):
    '''
    Combines all modules which eventually extract the raw URL from the provided link
    '''
    global extracted
    extracted = base64(redact(strip(decode(link))))
    print("\nExtracted Link:\n" + extracted)


def scan_url(raw_link):
    print("\nAnalyzing...\n")
    scanner = 'https://urlscan.io/api/v1/scan/'
    data = {"url": raw_link}
    headers = {"API-Key": api_key}
    p = requests.post(scanner, headers=headers, data=data)
    
    # allow time for urlscan.io to analyze link
    time.sleep(15)

    results_url = p.json()['api']
    r = requests.get(results_url)
    data = r.json()

    report_url = data['task']['reportURL']
    screenshot_url = data['task']['screenshotURL']

    print("Report: \n" + report_url)
    print("\nScreenshot: \n" + screenshot_url)


def main():
    parse()
    extract(base64)
    if needs_analysis:
        scan_url(extracted)


if __name__ == '__main__':
    main()
