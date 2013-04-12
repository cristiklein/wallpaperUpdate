#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import lxml.html
import os
import urllib
import urlparse

class ImageUrlNotFoundException(Exception):
	pass

#
# Initialize
#
logging.basicConfig(format='%(asctime)s %(message)s', level = logging.DEBUG)

#
# Parse command-line
#
# TODO
webpageUrl = 'http://apod.nasa.gov/apod/index.html'
outputFilename = os.path.expanduser('~/Desktop/apod-dynamic.jpg')

logging.debug("Webpage URL: " + webpageUrl)
logging.debug("Output filename: " + outputFilename)

#
# Download image
#

# Download and parse webpage
webpageDom = lxml.html.parse(webpageUrl)

imageUrls = [ e.attrib['src'] for e in webpageDom.findall('.//img') ]
if len(imageUrls) == 0:
	logging.error("No image URL found in base webpage.")
	raise ImageUrlNotFoundException()
if len(imageUrls) > 1:
	logging.warning("More than one image found in webpage, using the first.")

imageUrl = urlparse.urljoin(webpageUrl, imageUrls[0])
logging.debug("Found image URL: " + imageUrl)

# Download image
f = urllib.urlopen(imageUrl)
imageContent = f.read()
f.close()

# Write image (atomically)
tempFilename = outputFilename + ".tmp"
with open(tempFilename, 'w') as f:
	f.write(imageContent)
os.rename(tempFilename, outputFilename)

logging.debug("Done")
