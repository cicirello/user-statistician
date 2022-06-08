#
# user-statistician: Github action for generating a user stats card
# 
# Copyright (c) 2021-2022 Vincent A Cicirello
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
from TextLength import calculateTextLength, calculateTextLength110Weighted
import math

class StatsImageGenerator :
    """Generates an svg image from the collected stats."""

    headerTemplate = '<svg width="{1}" height="{0}" viewBox="0 0 {1} {0}" xmlns="http://www.w3.org/2000/svg" lang="{2}" xml:lang="{2}">'
    backgroundTemplate = '<rect x="2" y="2" stroke-width="4" rx="{4}" width="{3}" height="{0}" stroke="{1}" fill="{2}"/>'
    fontGroup = '<g font-weight="600" font-size="110pt" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision">'
    titleTemplate = '<text x="{3}" y="{4}" lengthAdjust="spacingAndGlyphs" textLength="{5}" transform="scale({2})" fill="{1}">{0}</text>'
    groupHeaderTemplate = '<g transform="translate(0, {0})" fill="{1}">'
    tableEntryTemplate = """<g transform="translate(15, {0})">
{1}
<g transform="scale({2})">
<text lengthAdjust="spacingAndGlyphs" textLength="{8}" x="{5}" y="{3}">{4}</text>
<text lengthAdjust="spacingAndGlyphs" textLength="{9}" x="{7}" y="{3}">{6}</text>
<text lengthAdjust="spacingAndGlyphs" textLength="{12}" x="{11}" y="{3}">{10}</text>
</g></g>"""
    tableEntryTemplateOneColumn = """<g transform="translate(15, {0})">
{1}
<g transform="scale({2})">
<text lengthAdjust="spacingAndGlyphs" textLength="{8}" x="{5}" y="{3}">{4}</text>
<text lengthAdjust="spacingAndGlyphs" textLength="{9}" x="{7}" y="{3}">{6}</text>
</g></g>"""
    tableHeaderTemplate = """<g transform="translate(15, 0)">
<g transform="scale({0})">
<text x="0" y="{1}" textLength="{3}" lengthAdjust="spacingAndGlyphs">{2}</text>
<text x="{5}" y="{1}" textLength="{6}" lengthAdjust="spacingAndGlyphs">{4}</text>
<text x="{8}" y="{1}" textLength="{9}" lengthAdjust="spacingAndGlyphs">{7}</text>
</g></g>"""
    tableHeaderTemplateOneColumn = """<g transform="translate(15, 0)">
<g transform="scale({0})">
<text x="0" y="{1}" textLength="{3}" lengthAdjust="spacingAndGlyphs">{2}</text>
<text x="{5}" y="{1}" textLength="{6}" lengthAdjust="spacingAndGlyphs">{4}</text>
</g></g>"""
    tableHeaderTemplateNoColumns = """<g transform="translate(15, 0)">
<g transform="scale({0})">
<text x="0" y="{1}" textLength="{3}" lengthAdjust="spacingAndGlyphs">{2}</text>
</g></g>"""
    languageEntryTemplate = """<g transform="translate(15, {0})">
<rect x="0.5" y="0.5" rx="2" width="15" height="15" fill="{1}" stroke-width="1" stroke="{2}"/>
<text transform="scale({4})" x="{5}" y="{6}" textLength="{7}" lengthAdjust="spacingAndGlyphs">{3}</text>
</g>"""
    languageEntryTemplateTwoLangs = """<g transform="translate(15, {0})">
<rect x="0.5" y="0.5" rx="2" width="15" height="15" fill="{1}" stroke-width="1" stroke="{2}"/>
<text transform="scale({4})" x="{5}" y="{6}" textLength="{7}" lengthAdjust="spacingAndGlyphs">{3}</text>
<rect x="{9}" y="0.5" rx="2" width="15" height="15" fill="{8}" stroke-width="1" stroke="{2}"/>
<text transform="scale({4})" x="{11}" y="{6}" textLength="{12}" lengthAdjust="spacingAndGlyphs">{10}</text>
</g>"""
    languageStringTemplate = "{0} {1:.2f}%"
    pieTransform = """<g transform="translate({2}, {1})">{0}</g>"""
    pieContrast = """<g transform="translate({3}, {1})"><circle cx="{0}" cy="{0}" r="{0}" fill="{2}"/></g>"""
    
    __slots__ = [
        '_stats',
        '_colors',
        '_height',
        '_width',
        '_rows',
        '_lineHeight',
        '_margin',
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
        '_includeTitle',
        '_exclude'
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
                 includeTitle,
                 exclude) :
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
        width - The minimum width of the SVG, but will autosize larger as needed.
        customTitle - If not None, this is used as the title, otherwise title is formed
            from user's name.
        includeTitle - If True inserts a title.
        exclude - A set of keys to exclude.
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
        self._exclude = exclude
        self._animateLanguageChart = animateLanguageChart
        self._animationSpeed = animationSpeed
        self._margin = 15 # CAUTION: Some templates currently have margin hardcoded to 15 (refactor before changing here)
        self._height = 0
        self._width = max(
            width,
            self.calculateMinimumFeasibleWidth()
            )
        self._firstColX = (self._width // 2)
        self._secondColX = self._firstColX + (self._width // 4) 
        self._lineHeight = 21
        self._pieRadius = (((self._width // 2 - self._margin) // self._lineHeight * self._lineHeight) - (self._lineHeight - 16)) // 2 
        self._rows = [
            StatsImageGenerator.headerTemplate,
            StatsImageGenerator.backgroundTemplate,
            StatsImageGenerator.fontGroup
            ]

    def calculateMinimumFeasibleWidth(self) :
        """Calculates the minimum feasible width for the
        SVG based on the lengths of the labels of the
        stats that are to be included, the category headings,
        and the title (if any), factoring in the chosen locale.
        """
        length = 0
        if self._includeTitle :
            length = calculateTextLength(self._title, self._titleSize, True, 600) + 2 * self._margin
        for category in self._categoryOrder :
            if category not in self._exclude :
                if category == "languages" :
                    languageData = self._stats.getStatsByKey(category)
                    if languageData["totalSize"] > 0 :
                        headingRowLength = calculateTextLength(
                            categoryLabels[self._locale][category]["heading"],
                            14,
                            True,
                            600)
                        headingRowLength += 2 * self._margin
                        length = max(length, headingRowLength)
                        for lang in languageData["languages"] :
                            langStr = StatsImageGenerator.languageStringTemplate.format(
                                lang[0],
                                100 * lang[1]["percentage"]
                                )
                            langRowLength = calculateTextLength(
                                langStr,
                                14,
                                True,
                                600
                                )
                            length = max(
                                length,
                                (langRowLength + 25 + (2 * self._margin)) * 2
                                )
                else :
                    keys = self.filterKeys(
                        self._stats.getStatsByKey(category),
                        statsByCategory[category]
                        )
                    if len(keys) > 0 :
                        headerRow = categoryLabels[self._locale][category]
                        headingRowLength = calculateTextLength(
                            headerRow["heading"],
                            14,
                            True,
                            600)
                        headingRowLength += 2 * self._margin
                        if headerRow["column-one"] != None :
                            headingRowLength *= 2
                        length = max(length, headingRowLength)
                        if headerRow["column-one"] != None :
                            length = max(
                                length,
                                4*(self._margin + calculateTextLength(
                                    headerRow["column-one"],
                                    14,
                                    True,
                                    600))
                                )
                        if headerRow["column-two"] != None :
                            length = max(
                                length,
                                4*(self._margin + calculateTextLength(
                                    headerRow["column-two"],
                                    14,
                                    True,
                                    600))
                                )
                        data = self._stats.getStatsByKey(category)
                        for k in keys :
                            labelLength = calculateTextLength(
                                statLabels[k]["label"][self._locale],
                                14,
                                True,
                                600)
                            length = max(
                                length,
                                (labelLength + 25 + (2 * self._margin)) * 2
                                )
                            if len(data[k]) == 1 and not self.isInt(data[k][0]) :
                                dataLength = calculateTextLength(
                                    data[k][0],
                                    14,
                                    True,
                                    600)
                                length = max(
                                    length,
                                    2*(dataLength + (2 * self._margin))
                                    )
        return math.ceil(length)

    def generateImage(self) :
        """Generates and returns the image."""
        self.insertTitle()
        for category in self._categoryOrder :
            if category not in self._exclude :
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
                            statsByCategory[category]
                            )
                        )
        self.finalizeImageData()
        return "".join(self._rows).replace("\n", "")

    def filterKeys(self, data, keys) :
        """Returns a list of the keys that have non-zero data and which are not excluded.

        Keyword arguments:
        data - The data (either contrib or repo data)
        keys - The list of keys relevant for the table.
        """
        return [ k for k in keys if (k not in self._exclude) and (k in data) and ((not self.isInt(data[k][0])) or data[k][0] > 0 or (len(data[k]) > 1 and data[k][1] > 0)) ]

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
            scale = round(0.75 * self._titleSize / 110, 3)
            titleTextLength = round(calculateTextLength110Weighted(self._title, 600))
            self._rows.append(
                StatsImageGenerator.titleTemplate.format(
                    self._title,
                    self._colors["title"],
                    "{0:.3f}".format(scale),
                    round(self._firstColX/scale - titleTextLength/2), #str(round(self._margin/scale)),
                    str(round(37/scale)),
                    titleTextLength
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
            scale = round(0.75 * 14 / 110, 3)
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
                    "{0:.3f}".format(scale),
                    str(round(12.5/scale)),
                    headerRow["heading"],
                    round(calculateTextLength110Weighted(headerRow["heading"], 600)),
                    headerRow["column-one"],
                    str(round(self._firstColX/scale)),
                    round(calculateTextLength110Weighted(headerRow["column-one"], 600)),
                    headerRow["column-two"],
                    str(round(self._secondColX/scale)),
                    round(calculateTextLength110Weighted(headerRow["column-two"], 600))
                    ))
                offset = self._lineHeight
            else :
                offset = 0
            for k in keys :
                template = StatsImageGenerator.tableEntryTemplate if len(data[k]) > 1 else StatsImageGenerator.tableEntryTemplateOneColumn   
                label = statLabels[k]["label"][self._locale]
                data1 = str(self.formatCount(data[k][0]))
                data2 = str(self.formatCount(data[k][1])) if len(data[k]) > 1 else ""
                if "totalIsLowerBound" in statLabels[k] and statLabels[k]["totalIsLowerBound"] :
                    data2 = "≥" + data2
                self._rows.append(template.format(
                    str(offset),
                    statLabels[k]["icon"].format(self._colors["icons"]),
                    "{0:.3f}".format(scale),
                    str(round(12.5/scale)),
                    label,
                    str(round(25/scale)),
                    data1,
                    str(round(self._firstColX/scale)),
                    round(calculateTextLength110Weighted(label, 600)),
                    round(calculateTextLength110Weighted(data1, 600)),
                    data2,
                    str(round(self._secondColX/scale)),
                    round(calculateTextLength110Weighted(data2, 600))
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
            scale = round(0.75 * 14 / 110, 3)
            self._height += self._lineHeight
            self._rows.append(
                StatsImageGenerator.groupHeaderTemplate.format(
                    self._height,
                    self._colors["text"]
                    )
                )
            self._rows.append(
                StatsImageGenerator.tableHeaderTemplateNoColumns.format(
                    "{0:.3f}".format(scale),
                    str(round(12.5/scale)),
                    categoryHeading,
                    round(calculateTextLength110Weighted(categoryHeading, 600))
                    )
                )
            offset = self._lineHeight
            self._rows.append(
                StatsImageGenerator.pieContrast.format(
                    self._pieRadius,
                    str(offset),
                    self._highContrast,
                    self._firstColX + self._margin
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
                    self._firstColX + self._margin + 1
                    )
                )
            diameter = self._pieRadius * 2
            numRowsToLeft = round(diameter / self._lineHeight)
            for i, L in enumerate(languageData["languages"]) :
                if i < numRowsToLeft :
                    lang = StatsImageGenerator.languageStringTemplate.format(
                        L[0],
                        100 * L[1]["percentage"]
                        )
                    self._rows.append(
                        StatsImageGenerator.languageEntryTemplate.format(
                            str(offset),
                            L[1]["color"],
                            self._highContrast,
                            lang,
                            "{0:.3f}".format(scale),
                            str(round(25/scale)),
                            str(round(12.5/scale)),
                            round(calculateTextLength110Weighted(lang, 600))
                            )
                        )
                    offset += self._lineHeight
                else :
                    break
            for j in range(numRowsToLeft, len(languageData["languages"]), 2) :
                L = languageData["languages"][j]
                lang = StatsImageGenerator.languageStringTemplate.format(
                    L[0],
                    100 * L[1]["percentage"]
                    )
                if j+1 < len(languageData["languages"]) :
                    L2 = languageData["languages"][j+1]
                    lang2 = StatsImageGenerator.languageStringTemplate.format(
                        L2[0],
                        100 * L2[1]["percentage"]
                        )
                    self._rows.append(
                        StatsImageGenerator.languageEntryTemplateTwoLangs.format(
                            str(offset),
                            L[1]["color"],
                            self._highContrast,
                            lang,
                            "{0:.3f}".format(scale),
                            str(round(25/scale)),
                            str(round(12.5/scale)),
                            round(calculateTextLength110Weighted(lang, 600)),
                            L2[1]["color"], 
                            self._firstColX + 0.5,
                            lang2,
                            str(round((self._firstColX + 25)/scale)),
                            round(calculateTextLength110Weighted(lang2, 600))
                            )
                        )
                    offset += self._lineHeight
                else :
                    self._rows.append(
                        StatsImageGenerator.languageEntryTemplate.format(
                            str(offset),
                            L[1]["color"],
                            self._highContrast,
                            lang,
                            "{0:.3f}".format(scale),
                            str(round(25/scale)),
                            str(round(12.5/scale)),
                            round(calculateTextLength110Weighted(lang, 600))
                            )
                        )
                    offset += self._lineHeight
            self._rows.append("</g>")
            if diameter + self._lineHeight + self._lineHeight - self._margin - 1 <= offset :
                self._height += offset
            else :
                self._height += diameter + self._lineHeight + self._lineHeight - self._margin - 1

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
        self._rows[0] = self._rows[0].format(str(self._height), str(self._width), self._locale)
        self._rows[1] = self._rows[1].format(
            str(self._height - 4),
            self._colors["border"],
            self._colors["bg"],
            str(self._width - 4),
            self._radius
            )
        self._rows.append("</g>\n</svg>\n")
        
