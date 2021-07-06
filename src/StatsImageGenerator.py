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


class StatsImageGenerator :
    """Generates an svg image from the collected stats."""

    headerTemplate = '<svg width="350" height="{0}" viewBox="0 0 350 {0}" xmlns="http://www.w3.org/2000/svg">'
    backgroundTemplate = '<rect x="1" y="1" stroke-width="2" rx="5" width="348" height="{0}" stroke="{1}" fill="{2}" />'
    fontGroup = '<g font-weight="600" font-family="Verdana,Geneva,DejaVu Sans,sans-serif">'
    titleTemplate = '<text x="15" y="35" font-size="16px" fill="{1}">{0}</text>'
    
    __slots__ = [
        '_stats',
        '_colors',
        '_height',
        '_rows'
        ]

    def __init__(self, stats, colors) :
        """Initializes the StatsImageGenerator.

        Keyword arguments:
        stats - An object of the Statistician class.
        colors - A dictionary containing the color theme.
        """
        self._stats = stats
        self._colors = colors
        self._height = 0
        self._rows = [
            StatsImageGenerator.headerTemplate,
            StatsImageGenerator.backgroundTemplate,
            StatsImageGenerator.fontGroup
            ]

    def generateImage(self, includeTitle, customTitle) :
        """Generates and returns the image.

        Keyword arguments:
        includeTitle - If True inserts a title.
        customTitle - If not None, this is used as the title, otherwise title is formed
            from user's name.
        """
        self.insertTitle(includeTitle, customTitle)
        self.finalizeImageData()
        return "\n".join(self._rows)

    def insertTitle(self, includeTitle, customTitle) :
        """Generates, formats, and inserts title.

        Keyword arguments:
        includeTitle - If True generates, formats, and inserts the title.
        customTitle - If not None, this is used as the title, otherwise title is formed
            from user's name.
        """
        if includeTitle :
            if customTitle != None :
                title = customTitle
            else :
                title = "{0}'s Activity".format(self._stats._name)
            self._rows.append(StatsImageGenerator.titleTemplate.format(title, self._colors["title"]))
            self._height += 35

    def insertGroup(self, data, exclude, headerRow, keys) :
        pass
        

    def finalizeImageData(self) :
        """Inserts the height into the svg opening tag and the rect for the background.
        Also inserts the border and background colors into the rect for the background.
        Must be called after generating the rest of the image since we won't know
        height until the end.  Also inserts closing tags.
        """
        self._height += 25
        self._rows[0] = self._rows[0].format(str(self._height))
        self._rows[1] = self._rows[1].format(
            str(self._height - 2),
            self._colors["border"],
            self._colors["bg"])
        self._rows.append("</g>\n</svg>\n")
        
