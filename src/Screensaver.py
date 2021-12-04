#!/usr/bin/env python3

"""
This script is triggered from a cron job to change the background image.
So you can repeatedly change the background image automatically.

"""
from Display import Display #einkommentieren befor das auf den pi geschoben wird


myDisplay = Display()   #einkommentieren befor das auf den pi geschoben wird
myDisplay.drawScreensaver()
