"""
permaize.py
Take a PDF, extract hyperlinks, and archive them.
Input: a PDF file
Output: Links to archives of all URLs found in PDF file, one per line

Problems:
* Many links are truncated at line-breaks. Need to look into detecting
  these and dealing with them.
"""

import click
import json
import logging
import re
import requests
from chalk import log


# Set up colorful logging
logger = logging.getLogger(__name__)
handler = log.ChalkHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Other constants
LINK_RE_PATTERN = r"(http[s]?\:\/\/[\w\/\.\-\?\=]+)"
link_re = re.compile(LINK_RE_PATTERN, (re.M | re.I))
TEST_TEXT_FILE = "sample-full.txt"
TEST_PDF_FILE = "sample.pdf"
PERMA_API_KEY_FILE = "perma_api_key.txt"


def get_test_text():
    test_f = open(TEST_TEXT_FILE)
    text = test_f.readlines()
    test_f.close()
    return text


def extract_text_from_pdf(f):
    """
    Extracts text from a PDF file with pdfminer
    """
    pass


def test_link_extraction_from_text():
    logger.debug("test_link_extraction_from_text() called")
    text = get_test_text()
    links = extract_hyperlinks_from_text(text)
    # print(links)
    return links


def clean_link(dirty_url):
    s = dirty_url.strip()
    s = s.rstrip('.')
    return s


def extract_hyperlinks_from_text(text):
    """
    Given an array of strings, find all hyperlinks.
    Returns a list of URLs found.
    """
    logger.debug("extract_hyperlinks_from_text() called on %d lines of text" % len(text))
    ret = []
    for line in text:
        # logger.debug("Text: %s" % (line))
        results = link_re.search(line)
        if results:
            result_texts = results.groups()
            for result_text in result_texts:
                cleaned = clean_link(result_text)
                logger.debug("Result: %s" % (cleaned))
                ret.append(cleaned)
    logger.info("Found %d hyperlinks" % (len(ret)))
    return ret


def get_perma_api_key():
    api_f = open(PERMA_API_KEY_FILE, 'r')
    api_key = api_f.read().strip()
    logger.debug("Got API key: <%s>" % (api_key))
    return api_key


def archive_link(url, title=None):
    """
    Archive a given URL to perma.cc.
    Returns a perma.cc URL.
    Adapted from: https://github.com/schollz/prevent-link-rot/blob/master/lib.py#L35
    """
    key = get_perma_api_key()

    if title is None:
        title = url

    payload = {'url': url, 'title': url}
    permacc_url = 'https://api.perma.cc/v1/archives/?api_key=' + key

    r = requests.post(permacc_url, data=json.dumps(payload))
    logger.debug("HTTP status code from perma.cc: %s" % (r.status_code))

    if r.status_code == 201:
        result = json.loads(r.text)
        print json.dumps(result, indent=4)
        logger.info(json.dumps(result))
        archive_url = str('http://perma.cc/' + result['guid'] + '?type=source')
        return archive_url
    else:
        logger.error("Bad status code %s" % (r.status_code))
        return None


@click.command()
@click.argument('input', type=click.File('rb'))
def links(input):
    """
    Show extracted hyperlinks, but don't archive.
    """
    # Extract text from PDF
    # Extract links from text
    # Show output
    pass


@click.command()
@click.argument('input', type=click.File('rb'))
def archive(input):
    """
    Extract links and archive them. Default command.
    """
    # Extract text from PDF
    # Extract links from text
    # Archive links
    # Show output
    pass


def main():
    # pass
    test_links = test_link_extraction_from_text()
    assert len(test_links) == 39, "Didn't get expected number of links"
    url = test_links[0]  # get first link
    test_archive = archive_link(url)

if __name__ == '__main__':
    main()
