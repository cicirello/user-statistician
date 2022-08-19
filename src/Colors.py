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



# Notes on the included themes:
#
# The light, dark, and dark-dimmed themes are based on
# GitHub's themes, and color-palette (see
# https://primer.style/primitives/colors).
#
# Specifically, from the link above we use:
# * background color (bg): canvas.inset
# * border color: accent.muted
# * icons: accent.emphasis
# * text: fg.default                      
# * title: accent.fg
#
# Notes to Potential Contributors:
#
# (1) For those who want to contribute a theme,
#     please check the combination of your background
#     color with text color, and background with title
#     color for accessibility at this site,
#     https://colorable.jxnblk.com/, and make sure the
#     combination has a rating of at least AA. You can also
#     simply run the test cases, which will automatically
#     verify that the text color and the background color have
#     a contrast ratio of at least 4.5:1, which is AA.
#     The contrast ratio between the background and title
#     colors should also be at least 4.5:1 (also enforced by test cases).
#
# (2) Before contributing a new color theme, ask yourself
#     whether it will likely have broad appeal or a narrow
#     audience. For example, if it is just the color palette
#     of your personal website or blog, then a theme may not
#     be necessary. You can simply use the colors input for
#     your usage.
#
# (3) Is it similar to one of the existing themes? Or does it
#     provide users with something truly new to choose from?
#
# (4) Please add the new theme alphabetized by theme name.
#
# (5) Include a comment with your GitHub userid indicating you
#     are the contributor of the theme (see the existing themes).
#
# (6) You can use either 3-digit hex, 6-digit hex, or named colors.
#
# (7) The existing test cases will automatically test that your
#     colors are valid hex, or valid named colors.
#     See https://developer.mozilla.org/en-US/docs/Web/CSS/color_value
#     for list of named colors.

colorMapping = {
    # Contributor: cicirello (part of initial theme set)
    "dark" : {
        "bg" : "#010409",
        "border" : "rgba(56,139,253,0.4)",
        "icons" : "#1f6feb",
        "text" : "#c9d1d9",
        "title" : "#58a6ff",
        "title-icon" : "github"
    },

    # Contributor: cicirello (updated theme set)
    "dark-colorblind" : {
        "bg" : "#010409",
        "border" : "rgba(56,139,253,0.4)",
        "icons" : "#1f6feb",
        "text" : "#c9d1d9",
        "title" : "#58a6ff",
        "title-icon" : "github"
    },

    # Contributor: cicirello (part of initial theme set)
    "dark-dimmed" : {
        "bg" : "#1c2128",
        "border" : "rgba(65,132,228,0.4)",
        "icons" : "#316dca",
        "text" : "#adbac7",
        "title" : "#539bf5",
        "title-icon" : "github"
    },

    # Contributor: cicirello (updated theme set)
    "dark-high-contrast" : {
        "bg" : "#010409",
        "border" : "#409eff",
        "icons" : "#409eff",
        "text" : "#f0f3f6",
        "title" : "#71b7ff",
        "title-icon" : "github"
    },

    # Contributor: cicirello (updated theme set)
    "dark-tritanopia" : {
        "bg" : "#010409",
        "border" : "rgba(56,139,253,0.4)",
        "icons" : "#1f6feb",
        "text" : "#c9d1d9",
        "title" : "#58a6ff",
        "title-icon" : "github"
    },

    # Contributor: cicirello (part of initial theme set)
    "light" : {
        "bg" : "#f6f8fa",
        "border" : "rgba(84,174,255,0.4)",
        "icons" : "#0969da",
        "text" : "#24292f",
        "title" : "#0969da",
        "title-icon" : "github"
    },

    # Contributor: cicirello (updated theme set)
    "light-colorblind" : {
        "bg" : "#f6f8fa",
        "border" : "rgba(84,174,255,0.4)",
        "icons" : "#0969da",
        "text" : "#24292f",
        "title" : "#0969da",
        "title-icon" : "github"
    },

    # Contributor: cicirello (updated theme set)
    "light-high-contrast" : {
        "bg" : "#ffffff",
        "border" : "#368cf9",
        "icons" : "#0349b4",
        "text" : "#0E1116",
        "title" : "#0349b4",
        "title-icon" : "github"
    },

    # Contributor: cicirello (updated theme set)
    "light-tritanopia" : {
        "bg" : "#f6f8fa",
        "border" : "rgba(84,174,255,0.4)",
        "icons" : "#0969da",
        "text" : "#24292f",
        "title" : "#0969da",
        "title-icon" : "github"
    },
}

# These are template strings for the icons available for the title line.
# Each color theme has an associated icon. User can also override the default
# for the theme by name.
#
# The template strings each have up to 3 inputs, {0}, {1}, and {2}.
# {0} is the x position in pixels.
# {1} is the y position in pixels.
# {2}, if present, is the fill color, which will be populated with the high
#    contrasting color relative to the background (e.g., for github, it will
#    either be white or black depending upon background, which is consistent
#    with GitHub's logo usage guidelines.
iconTemplates = {
    "github" : """<svg x="{0}" y="{1}" width="32" height="32" viewBox="0 0 16 16"><path fill="{2}" fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>""",
}
