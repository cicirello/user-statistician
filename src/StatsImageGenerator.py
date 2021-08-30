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

from StatConfig import *
from PieChart import svgPieChart
from ColorUtil import highContrastingColor

class StatsImageGenerator :
    """Generates an svg image from the collected stats."""

    headerTemplate = '<svg width="{1}" height="{0}" viewBox="0 0 {1} {0}" xmlns="http://www.w3.org/2000/svg">'
    backgroundTemplate = '<rect x="2" y="2" stroke-width="4" rx="{4}" width="{3}" height="{0}" stroke="{1}" fill="{2}"/>'
    fontGroup = '<g font-weight="600" font-family="Verdana,Geneva,DejaVu Sans,sans-serif">'
    titleTemplate = '<text x="15" y="37" font-size="{2}px" fill="{1}">{0}</text>'
    groupHeaderTemplate = '<g transform="translate(0, {0})" font-size="14px" fill="{1}">'
    tableEntryTemplate = """<g transform="translate(15, {0})">
{2}
<text x="25" y="12.5">{3}:</text>
<text x="{6}" y="12.5">{4}</text>
<text x="{7}" y="12.5">{5}</text>
</g>"""
    tableEntryTemplateOneColumn = """<g transform="translate(15, {0})">
{2}
<text x="25" y="12.5">{3}:</text>
<text x="{6}" y="12.5">{4}</text>
</g>"""
    tableHeaderTemplate = """<g transform="translate(15, 0)">
<text x="0" y="12.5">{0}:</text>
<text x="{3}" y="12.5">{1}</text>
<text x="{4}" y="12.5">{2}</text>
</g>"""
    tableHeaderTemplateOneColumn = """<g transform="translate(15, 0)">
<text x="0" y="12.5">{0}:</text>
<text x="{3}" y="12.5">{1}</text>
</g>"""
    tableHeaderTemplateNoColumns = """<g transform="translate(15, 0)">
<text x="0" y="12.5">{0}:</text>
</g>"""
    languageEntryTemplate = """<g transform="translate(15, {0})">
<rect x="0.5" y="0.5" rx="2" width="15" height="15" fill="{1}" stroke-width="1" stroke="{4}"/>
<text x="25" y="12.5">{2} {3:.2f}%</text>
</g>"""
    languageEntryTemplateTwoLangs = """<g transform="translate(15, {0})">
<rect x="0.5" y="0.5" rx="2" width="15" height="15" fill="{1}" stroke-width="1" stroke="{4}"/>
<text x="25" y="12.5">{2} {3:.2f}%</text>
<rect x="{8}" y="0.5" rx="2" width="15" height="15" fill="{5}" stroke-width="1" stroke="{4}"/>
<text x="{9}" y="12.5">{6} {7:.2f}%</text>
</g>"""
    pieTransform = """<g transform="translate({2}, {1})">{0}</g>"""
    pieContrast = """<g transform="translate({3}, {1})"><circle cx="{0}" cy="{0}" r="{0}" fill="{2}"/></g>"""
    
    __slots__ = [
        '_stats',
        '_colors',
        '_height',
        '_width',
        '_rows',
        '_lineHeight',
        '_locale',
        '_radius',
        '_titleSize',
        '_pieRadius',
        '_highContrast',
        '_categoryOrder',
        '_animateLanguageChart',
        '_animationSpeed',
        '_firstColX',
        '_secondColX',
        '_title',
        '_includeTitle'
        ]

    def __init__(self,
                 stats,
                 colors,
                 locale,
                 radius,
                 titleSize,
                 categories,
                 animateLanguageChart,
                 animationSpeed,
                 width,
                 customTitle,
                 includeTitle) :
        """Initializes the StatsImageGenerator.

        Keyword arguments:
        stats - An object of the Statistician class.
        colors - A dictionary containing the color theme.
        locale - The 2-character locale code.
        radius - The border radius.
        titleSize - The font size for the title.
        categories - List of category keys in order they should appear on card.
        animateLanguageChart - Boolean controlling whether to animate the language pie chart.
        animationSpeed - An integer duration for one full rotation of language pie chart.
        width - The width of the SVG, preferably divisible by 4.
        customTitle - If not None, this is used as the title, otherwise title is formed
            from user's name.
        includeTitle - If True inserts a title.
        """
        self._stats = stats
        self._colors = colors
        self._highContrast = highContrastingColor(self._colors["bg"])
        self._locale = locale
        self._radius = radius
        self._titleSize = titleSize
        if customTitle != None :
            self._title = customTitle
        else :
            self._title = titleTemplates[self._locale].format(self._stats._name)
        self._includeTitle = includeTitle
        self._categoryOrder = categories
        self._animateLanguageChart = animateLanguageChart
        self._animationSpeed = animationSpeed
        self._height = 0
        self._width = width
        self._firstColX = (self._width // 2) - 15
        self._secondColX = self._firstColX + (self._width // 4) 
        self._lineHeight = 21
        self._pieRadius = (((self._width // 2 - 15) // self._lineHeight * self._lineHeight) - (self._lineHeight - 16)) // 2 
        self._rows = [
            StatsImageGenerator.headerTemplate,
            StatsImageGenerator.backgroundTemplate,
            StatsImageGenerator.fontGroup
            ]

    def generateImage(self, exclude) :
        """Generates and returns the image.

        Keyword arguments:
        exclude - Set of keys to exclude.
        """
        self.insertTitle()
        for category in self._categoryOrder :
            if category not in exclude :
                if category == "languages" :
                    self.insertLanguagesChart(
                        self._stats.getStatsByKey(category),
                        categoryLabels[self._locale][category]["heading"]
                        )
                else :
                    self.insertGroup(
                        self._stats.getStatsByKey(category),
                        categoryLabels[self._locale][category],
                        self.filterKeys(
                            self._stats.getStatsByKey(category),
                            exclude,
                            statsByCategory[category]
                            )
                        )
        self.finalizeImageData()
        return "".join(self._rows).replace("\n", "")

    def filterKeys(self, data, exclude, keys) :
        """Returns a list of the keys that have non-zero data and which are not excluded.

        Keyword arguments:
        data - The data (either contrib or repo data)
        exclude - A set of keys to exclude
        keys - The list of keys relevant for the table.
        """
        return [ k for k in keys if (k not in exclude) and (k in data) and ((not self.isInt(data[k][0])) or data[k][0] > 0 or (len(data[k]) > 1 and data[k][1] > 0)) ]

    def isInt(self, value) :
        """Checks if a value is an int.

        Keyword arguments:
        value - The value to check.
        """
        try:
            int(value)
        except:
            return False
        return True

    def insertTitle(self) :
        """Generates, formats, and inserts title."""
        if self._includeTitle :
            self._rows.append(
                StatsImageGenerator.titleTemplate.format(
                    self._title,
                    self._colors["title"],
                    str(self._titleSize)
                    )
                )
            self._height += 39

    def insertGroup(self, data, headerRow, keys) :
        """Generates the portion of the image for a group
        (i.e., the repositories section or the contributions section).
        If there are no keys with data, then this does nothing (excludes
        all in group).

        Keyword arguments:
        data - A dictionary with the data.
        headerRow - A dictionary with the header row text. Pass None for no table header.
        keys - A list of keys in the order they should appear.
        """
        if len(keys) > 0 :
            self._height += self._lineHeight
            self._rows.append(StatsImageGenerator.groupHeaderTemplate.format(self._height, self._colors["text"]))
            if headerRow != None :
                if headerRow["column-one"] == None :
                    template = StatsImageGenerator.tableHeaderTemplateNoColumns
                elif headerRow["column-two"] == None :
                    template = StatsImageGenerator.tableHeaderTemplateOneColumn
                else :
                    template = StatsImageGenerator.tableHeaderTemplate  
                self._rows.append(template.format(
                    headerRow["heading"],
                    headerRow["column-one"],
                    headerRow["column-two"],
                    self._firstColX,
                    self._secondColX
                    ))
                offset = self._lineHeight
            else :
                offset = 0
            for k in keys :
                template = StatsImageGenerator.tableEntryTemplate if len(data[k]) > 1 else StatsImageGenerator.tableEntryTemplateOneColumn   
                self._rows.append(template.format(
                    str(offset),
                    self._colors["icons"], # no longer needed, but kept here to avoid need to renumber in templates
                    statLabels[k]["icon"].format(self._colors["icons"]),
                    statLabels[k]["label"][self._locale],
                    self.formatCount(data[k][0]),
                    self.formatCount(data[k][1]) if len(data[k]) > 1 else "",
                    self._firstColX,
                    self._secondColX
                    ))
                offset += self._lineHeight
            self._rows.append("</g>")
            self._height += offset

    def insertLanguagesChart(self, languageData, categoryHeading) :
        """Generates and returns the SVG section for the language
        distribution summary and pie chart.

        Keyword arguments:
        languageData - The language stats data
        categoryHeading - The heading for the section
        """
        if languageData["totalSize"] > 0 :
            self._height += self._lineHeight
            self._rows.append(
                StatsImageGenerator.groupHeaderTemplate.format(
                    self._height,
                    self._colors["text"]
                    )
                )
            self._rows.append(
                StatsImageGenerator.tableHeaderTemplateNoColumns.format(categoryHeading)
                )
            offset = self._lineHeight
            self._rows.append(
                StatsImageGenerator.pieContrast.format(
                    self._pieRadius,
                    str(offset),
                    self._highContrast,
                    self._firstColX + 15
                    )
                )
            self._rows.append(
                StatsImageGenerator.pieTransform.format(
                    svgPieChart(
                        [L[1] for L in languageData["languages"]],
                        self._pieRadius - 1,
                        self._animateLanguageChart,
                        self._animationSpeed
                        ),
                    str(offset+1),
                    self._firstColX + 16
                    )
                )
            diameter = self._pieRadius * 2
            numRowsToLeft = round(diameter / self._lineHeight)
            for i, L in enumerate(languageData["languages"]) :
                if i < numRowsToLeft :
                    self._rows.append(
                        StatsImageGenerator.languageEntryTemplate.format(
                            str(offset),
                            L[1]["color"], 
                            L[0],
                            100 * L[1]["percentage"],
                            self._highContrast
                            )
                        )
                    offset += self._lineHeight
                else :
                    break
            for j in range(numRowsToLeft, len(languageData["languages"]), 2) :
                L = languageData["languages"][j]
                if j+1 < len(languageData["languages"]) :
                    L2 = languageData["languages"][j+1]
                    self._rows.append(
                        StatsImageGenerator.languageEntryTemplateTwoLangs.format(
                            str(offset),
                            L[1]["color"], 
                            L[0],
                            100 * L[1]["percentage"],
                            self._highContrast,
                            L2[1]["color"], 
                            L2[0],
                            100 * L2[1]["percentage"],
                            self._firstColX + 0.5,
                            self._firstColX + 25
                            )
                        )
                    offset += self._lineHeight
                else :
                    self._rows.append(
                        StatsImageGenerator.languageEntryTemplate.format(
                            str(offset),
                            L[1]["color"], 
                            L[0],
                            100 * L[1]["percentage"],
                            self._highContrast
                            )
                        )
                    offset += self._lineHeight
            self._rows.append("</g>")
            if diameter + self._lineHeight + self._lineHeight - 16 <= offset :
                self._height += offset
            else :
                self._height += diameter + self._lineHeight + self._lineHeight - 16

    def formatCount(self, count) :
        """Formats the count.

        Keyword arguments:
        count - The count to format.
        """
        if (not self.isInt(count)) or count < 100000 :
            return count
        elif count < 1000000 :
            return "{0:.1f}K".format(count // 100 * 100 / 1000)
        else :
            # can such a real user exist?
            return "{0:.1f}M".format(count // 100000 * 100000 / 1000000)
        
    def finalizeImageData(self) :
        """Inserts the height into the svg opening tag and the rect for the background.
        Also inserts the border and background colors into the rect for the background.
        Must be called after generating the rest of the image since we won't know
        height until the end.  Also inserts closing tags.
        """
        self._height += self._lineHeight
        self._rows[0] = self._rows[0].format(str(self._height), str(self._width))
        self._rows[1] = self._rows[1].format(
            str(self._height - 4),
            self._colors["border"],
            self._colors["bg"],
            str(self._width - 4),
            self._radius
            )
        self._rows.append("</g>\n</svg>\n")
        
