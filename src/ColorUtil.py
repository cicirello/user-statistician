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

def isValidColor(color) :
    """Checks if a color is a valid color.

    Keyword arguments:
    color - The color to check, either in hex or as a named color or as an rgba().
    """
    validHexDigits = set("0123456789abcdefABCDEF")
    color = color.strip()
    if color.startswith("#") :
        if len(color) != 4 and len(color) != 7 :
            return False
        return all(c in validHexDigits for c in color[1:])
    elif color.startswith("rgba(") :
        return strToRGBA(color) != None
    else :
        return color in _namedColors

def strToRGBA(color) :
    """Converts a str specifying rgba color to
    r, g, b, and a channels. Returns (r, g, b, a) is valid
    and otherwise returns None.

    Keyword arguments:
    color - a str of the form: rgba(r,g,b,a).
    """
    if color.startswith("rgba(") :
        last = color.find(")")
        if last > 5 :
            rgba = color[5:last].split(",")
            if len(rgba) == 4 :
                try :
                    r = int(rgba[0])
                    g = int(rgba[1])
                    b = int(rgba[2])
                    a = float(rgba[3])
                except ValueError :
                    return None
                if r >= 256 :
                    r = 255
                if g >= 256 :
                    g = 255
                if b >= 256 :
                    b = 255
                if r < 0 :
                    r = 0
                if g < 0 :
                    g = 0
                if b < 0 :
                    b = 0
                if a < 0.0 :
                    a = 0.0
                if a > 1.0 :
                    a = 1.0
                return r, g, b, a
    return None

def highContrastingColor(color) :
    """Computes a highly contrasting color.
    Specifically, maximizes the contrast ratio. Contrast ratio is
    (L1 + 0.05) / (L2 + 0.05), where L1 and L2 are the luminances
    of the colors and L1 is the larger luminance. Returns None
    if color is not a valid hex color or named color.

    Keyword arguments:
    color - The color to contrast with, either in hex or as a named color.
    """
    L = luminance(color)
    if L == None :
        return None
    if (L + 0.05) / 0.05 >= 1.05 / (L + 0.05) :
        return "#000000" # black
    else :
        return "#ffffff" # white

def contrastRatio(c1, c2) :
    """Computes contrast ratio of a pair of colors.
    Returns the contrast ratio provided both colors are valid,
    and otherwise returns None.

    Keyword arguments:
    c1 - Color 1, in hex or as a named color.
    c2 - Color 2, in hex or as a named color.
    """
    L1 = luminance(c1)
    L2 = luminance(c2)
    if L1 == None or L2 == None :
        return None
    if L1 < L2 :
        L1, L2 = L2, L1
    return (L1 + 0.05) / (L2 + 0.05)

def luminance(color) :
    """Calculates the luminance of a color. Returns None
    if color is not a valid hex color or named color.

    Keyword arguments:
    color - The color, either in hex or as a named color.
    """
    color = color.strip()
    if color.startswith("rgba(") :
        rgba = strToRGBA(color)
        if rgba != None :
            r, g, b, a = rgba
        else :
            return None
    else :
        if not color.startswith("#") :
            if color not in _namedColors :
                return None
            color = _namedColors[color]
        if len(color) == 4 :
            r = color[1] + color[1]
            g = color[2] + color[2]
            b = color[3] + color[3]
        elif len(color) == 7 :
            r = color[1:3]
            g = color[3:5]
            b = color[5:7]
        else:
            return None
        r = int(r, base=16)
        g = int(g, base=16)
        b = int(b, base=16)
    r = _sRGBtoLin(r / 255)
    g = _sRGBtoLin(g / 255)
    b = _sRGBtoLin(b / 255)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def _sRGBtoLin(c) :
    """Transformation from
    https://developer.mozilla.org/en-US/docs/Web/Accessibility/Understanding_Colors_and_Luminance

    Keyword arguments:
    c - A color channel (i.e., r, g, or b)
    """
    if c <= 0.04045 :
        return c / 12.92
    else :
        return ((c + 0.055)/1.055) ** 2.4

# The SVG, CSS, etc named colors with their hex.
# See https://developer.mozilla.org/en-US/docs/Web/CSS/color_value.
# We need the hex that corresponds to the names in the event that the
# user specifies a color by name so that we can compute a high contrast
# color relative to background for the "Other" language category, or
# for languages without colors defined by Linguist.
_namedColors = {
    "aliceblue" : "#f0f8ff",
    "antiquewhite" : "#faebd7",
    "aqua" : "#00ffff",
    "aquamarine" : "#7fffd4",
    "azure" : "#f0ffff",
    "beige" : "#f5f5dc",
    "bisque" : "#ffe4c4",
    "black" : "#000000",
    "blanchedalmond" : "#ffebcd",
    "blue" : "#0000ff",
    "blueviolet" : "#8a2be2",
    "brown" : "#a52a2a",
    "burlywood" : "#deb887",
    "cadetblue" : "#5f9ea0",
    "chartreuse" : "#7fff00",
    "chocolate" : "#d2691e",
    "coral" : "#ff7f50",
    "cornflowerblue" : "#6495ed",
    "cornsilk" : "#fff8dc",
    "crimson" : "#dc143c",
    "cyan" : "#00ffff",
    "darkblue" : "#00008b",
    "darkcyan" : "#008b8b",
    "darkgoldenrod" : "#b8860b",
    "darkgray" : "#a9a9a9",
    "darkgreen" : "#006400",
    "darkgrey" : "#a9a9a9",
    "darkkhaki" : "#bdb76b",
    "darkmagenta" : "#8b008b",
    "darkolivegreen" : "#556b2f",
    "darkorange" : "#ff8c00",
    "darkorchid" : "#9932cc",
    "darkred" : "#8b0000",
    "darksalmon" : "#e9967a",
    "darkseagreen" : "#8fbc8f",
    "darkslateblue" : "#483d8b",
    "darkslategray" : "#2f4f4f",
    "darkslategrey" : "#2f4f4f",
    "darkturquoise" : "#00ced1",
    "darkviolet" : "#9400d3",
    "deeppink" : "#ff1493",
    "deepskyblue" : "#00bfff",
    "dimgray" : "#696969",
    "dimgrey" : "#696969",
    "dodgerblue" : "#1e90ff",
    "firebrick" : "#b22222",
    "floralwhite" : "#fffaf0",
    "forestgreen" : "#228b22",
    "fuchsia" : "#ff00ff",
    "gainsboro" : "#dcdcdc",
    "ghostwhite" : "#f8f8ff",
    "goldenrod" : "#daa520",
    "gold" : "#ffd700",
    "gray" : "#808080",
    "green" : "#008000",
    "greenyellow" : "#adff2f",
    "grey" : "#808080",
    "honeydew" : "#f0fff0",
    "hotpink" : "#ff69b4",
    "indianred" : "#cd5c5c",
    "indigo" : "#4b0082",
    "ivory" : "#fffff0",
    "khaki" : "#f0e68c",
    "lavenderblush" : "#fff0f5",
    "lavender" : "#e6e6fa",
    "lawngreen" : "#7cfc00",
    "lemonchiffon" : "#fffacd",
    "lightblue" : "#add8e6",
    "lightcoral" : "#f08080",
    "lightcyan" : "#e0ffff",
    "lightgoldenrodyellow" : "#fafad2",
    "lightgray" : "#d3d3d3",
    "lightgreen" : "#90ee90",
    "lightgrey" : "#d3d3d3",
    "lightpink" : "#ffb6c1",
    "lightsalmon" : "#ffa07a",
    "lightseagreen" : "#20b2aa",
    "lightskyblue" : "#87cefa",
    "lightslategray" : "#778899",
    "lightslategrey" : "#778899",
    "lightsteelblue" : "#b0c4de",
    "lightyellow" : "#ffffe0",
    "lime" : "#00ff00",
    "limegreen" : "#32cd32",
    "linen" : "#faf0e6",
    "magenta" : "#ff00ff",
    "maroon" : "#800000",
    "mediumaquamarine" : "#66cdaa",
    "mediumblue" : "#0000cd",
    "mediumorchid" : "#ba55d3",
    "mediumpurple" : "#9370db",
    "mediumseagreen" : "#3cb371",
    "mediumslateblue" : "#7b68ee",
    "mediumspringgreen" : "#00fa9a",
    "mediumturquoise" : "#48d1cc",
    "mediumvioletred" : "#c71585",
    "midnightblue" : "#191970",
    "mintcream" : "#f5fffa",
    "mistyrose" : "#ffe4e1",
    "moccasin" : "#ffe4b5",
    "navajowhite" : "#ffdead",
    "navy" : "#000080",
    "oldlace" : "#fdf5e6",
    "olive" : "#808000",
    "olivedrab" : "#6b8e23",
    "orange" : "#ffa500",
    "orangered" : "#ff4500",
    "orchid" : "#da70d6",
    "palegoldenrod" : "#eee8aa",
    "palegreen" : "#98fb98",
    "paleturquoise" : "#afeeee",
    "palevioletred" : "#db7093",
    "papayawhip" : "#ffefd5",
    "peachpuff" : "#ffdab9",
    "peru" : "#cd853f",
    "pink" : "#ffc0cb",
    "plum" : "#dda0dd",
    "powderblue" : "#b0e0e6",
    "purple" : "#800080",
    "rebeccapurple" : "#663399",
    "red" : "#ff0000",
    "rosybrown" : "#bc8f8f",
    "royalblue" : "#4169e1",
    "saddlebrown" : "#8b4513",
    "salmon" : "#fa8072",
    "sandybrown" : "#f4a460",
    "seagreen" : "#2e8b57",
    "seashell" : "#fff5ee",
    "sienna" : "#a0522d",
    "silver" : "#c0c0c0",
    "skyblue" : "#87ceeb",
    "slateblue" : "#6a5acd",
    "slategray" : "#708090",
    "slategrey" : "#708090",
    "snow" : "#fffafa",
    "springgreen" : "#00ff7f",
    "steelblue" : "#4682b4",
    "tan" : "#d2b48c",
    "teal" : "#008080",
    "thistle" : "#d8bfd8",
    "tomato" : "#ff6347",
    "turquoise" : "#40e0d0",
    "violet" : "#ee82ee",
    "wheat" : "#f5deb3",
    "white" : "#ffffff",
    "whitesmoke" : "#f5f5f5",
    "yellow" : "#ffff00",
    "yellowgreen" : "#9acd32"
    }
