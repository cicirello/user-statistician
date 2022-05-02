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
        "title" : "#58a6ff"
        },

    # Contributor: cicirello (part of initial theme set)
    "dark-dimmed" : {
        "bg" : "#1c2128",
        "border" : "rgba(65,132,228,0.4)",
        "icons" : "#316dca",
        "text" : "#adbac7",
        "title" : "#539bf5"
        },

    # Contributor: cicirello (part of initial theme set)
    "light" : {
        "bg" : "#f6f8fa",
        "border" : "rgba(84,174,255,0.4)",
        "icons" : "#0969da",
        "text" : "#24292f",
        "title" : "#0969da"
        }
    
    }
