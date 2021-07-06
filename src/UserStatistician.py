#!/usr/bin/env python3
#
# user-statistician: Github action for generating a user stats card
# 
# Copyright (c) 2021 Vincent A Cicirello
# https://www.cicirello.org/
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from Statistician import Statistician
from Colors import colorMapping
from StatsImageGenerator import StatsImageGenerator
import sys
import os

if __name__ == "__main__" :

    imageFilenameWithPath = sys.argv[1].strip()
    
    includeTitle = sys.argv[2].strip().lower() == "true"
    
    customTitle = sys.argv[3].strip()
    if len(customTitle) == 0 or not includeTitle :
        customTitle = None
        
    colors = sys.argv[4].strip().replace(",", " ").split()
    if len(colors) == 1 and colors[0] in colorMapping :
        # get theme colors
        colors = colorMapping[colors[0]]
    elif len(colors) < 4 :
        # default to light theme if invalid number of colors passed
        colors = colorMapping["light"]
    else :
        colors = { "bg" : colors[0],
                "border" : colors[1],
                "icons" : colors[2],
                "title" : colors[3],
                "text" : colors[4] if len(colors) > 4 else colors[3]
            }

    exclude = set(sys.argv[5].strip().replace(",", " ").split())

    failOnError = sys.argv[6].strip().lower() == "true"
    
    stats = Statistician(failOnError)
    generator = StatsImageGenerator(stats, colors)
    image = generator.generateImage(includeTitle, customTitle)
    print("Image")
    print(image)
    
    print("Contributions", stats._contrib)
    print("Contrib Years", stats._contributionYears)
    print("Followers", stats._followers)
    print("Repos", stats._repo)
    print("Name", stats._name)
    print("User", stats._login)
    
    print("::set-output name=exit-code::0")
    
