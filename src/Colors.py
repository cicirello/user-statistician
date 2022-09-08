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
# The template strings each have up to 4 inputs, {0}, {1}, {2}, and {3}.
# {0} is the width/height, i.e., it is square.
# {1} is the x position in pixels.
# {2} is the y position in pixels.
# {3}, if present, is the fill color, which will be populated with the high
#    contrasting color relative to the background (e.g., for github, it will
#    either be white or black depending upon background, which is consistent
#    with GitHub's logo usage guidelines.
iconTemplates = {
    "github" : """<svg x="{1}" y="{2}" width="{0}" height="{0}" viewBox="0 0 16 16"><path fill="{3}" fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>""",
    "pumpkin" : """<svg x="{1}" y="{2}" width="{0}" height="{0}" viewBox="8 8 84 84"><path fill="#FF7518" d="M80.3,30.7C74.9,27.3,68.9,27,66,28.3c0,0-0.1,0-0.1,0c-2.6-0.8-5.1-0.8-7.2-0.5c-0.8-2-0.8-3.8-0.1-5.2 c1.4-2.8,5.1-3.8,5.2-3.8c1-0.3,1.7-1.3,1.5-2.3l-0.9-4.4c-0.2-0.9-1-1.6-1.9-1.6c-7.2-0.2-12.8,1.7-16.5,5.7c-3.7,3.9-4.7,8.8-4.9,11.6c-2-0.2-4.4-0.2-6.8,0.6c0,0,0,0-0.1,0c-3-1.4-9-1-14.3,2.4C14.5,34.1,8.2,41.5,8.3,57.5c0.2,20.2,7,29.8,21.6,30.2c0.6,0.3,1.1,0.6,1.8,0.8c1.9,0.6,4.1,0.8,6.1,0.8c2.9,0,5.6-0.4,6.7-0.6c1.3,0.4,2.7,0.7,4.5,0.8c0,0,0.1,0,0.1,0c0.2,0,0.3,0,0.4-0.1c0.1,0,0.3,0.1,0.4,0.1c0,0,0.1,0,0.1,0c1.7-0.1,3.2-0.4,4.5-0.8c1.1,0.2,3.8,0.6,6.7,0.6c2,0,4.2-0.2,6.1-0.8c0.7-0.2,1.3-0.5,1.8-0.8c0.1,0,0.2,0,0.3,0c0,0,0,0,0,0c15-0.2,22-9.8,22.2-30.2C91.8,41.5,85.5,34.1,80.3,30.7z"/><path fill="#FFFF00" stroke="#FFFF00" stroke-width="4" d="M49.3,73.2C49.3,73.2,49.3,73.2,49.3,73.2C49.3,73.2,49.3,73.2,49.3,73.2c-12.7,0-16.6-7.3-17.8-11.9c5.7,2.7,11.6,4,17.8,4c0,0,0,0,0,0c0,0,0,0,0,0c0.5,0,0.9,0,1.4,0l0,3.3c0,0.6,0.3,1.1,0.7,1.5c0.4,0.4,1,0.5,1.6,0.4c0.1,0,0.9-0.1,1.9-0.3c3-0.5,4.3-0.7,4.5-0.7 c0.9-0.2,1.6-1,1.6-2l0-4c2.1-0.6,4.1-1.4,6.1-2.3C66,65.9,62.1,73.2,49.3,73.2z"/><path fill="#FFFF00" d="M31.4,54.6l12.4,2.8c0.1,0,0.3,0,0.4,0c0,0,0,0,0,0c1.1,0,2-0.9,2-2c0-0.3-0.1-0.6-0.2-0.8l-3.5-12.2c-0.2-0.7-0.8-1.2-1.5-1.4c-0.7-0.2-1.4,0.1-1.9,0.6l-8.9,9.8c-0.5,0.5-0.6,1.3-0.4,2S30.7,54.4,31.4,54.6z"/><path fill="#FFFF00" d="M54.4,57.4c0.1,0,0.3,0,0.4,0l12.4-2.8c0.7-0.2,1.3-0.7,1.5-1.3s0.1-1.4-0.4-2l-8.9-9.8c-0.5-0.5-1.2-0.8-1.9-0.6c-0.7,0.2-1.3,0.7-1.5,1.4l-3.5,12.5c-0.2,0.7,0,1.4,0.5,1.9C53.3,57.1,53.8,57.4,54.4,57.4z"/></svg>""",
}
