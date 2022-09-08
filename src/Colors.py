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

    # Contributor: cicirello (Halloween related themes)
    "halloween" : {
        "bg" : "#090B06",
        "border" : "#F5D913",
        "icons" : "#F46D0E",
        "text" : "#EB912D",
        "title" : "#F46D0E",
        "title-icon" : "pumpkin"
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
    "pumpkin" : """<svg x="{1}" y="{2}" width="{0}" height="{0}" viewBox="8 8 84 84"><path fill="#FF7518" d="M80.3 30.7C74.9 27.3 68.9 27 66 28.3h-.1c-2.6-.8-5.1-.8-7.2-.5-.8-2-.8-3.8-.1-5.2 1.4-2.8 5.1-3.8 5.2-3.8 1-.3 1.7-1.3 1.5-2.3l-.9-4.4a2 2 0 0 0-1.9-1.6c-7.2-.2-12.8 1.7-16.5 5.7a19 19 0 0 0-4.9 11.6c-2-.2-4.4-.2-6.8.6h-.1c-3-1.4-9-1-14.3 2.4-5.4 3.3-11.7 10.7-11.6 26.7.2 20.2 7 29.8 21.6 30.2.6.3 1.1.6 1.8.8 1.9.6 4.1.8 6.1.8 2.9 0 5.6-.4 6.7-.6 1.3.4 2.7.7 4.5.8h.1l.4-.1.4.1h.1a19 19 0 0 0 4.5-.8c1.1.2 3.8.6 6.7.6 2 0 4.2-.2 6.1-.8.7-.2 1.3-.5 1.8-.8h.3c15-.2 22-9.8 22.2-30.2.2-16-6.1-23.4-11.3-26.8z"/><path fill="#FF0" stroke="#FF0" stroke-width="4" d="M49.3 73.2c-12.7 0-16.6-7.3-17.8-11.9a41 41 0 0 0 17.8 4h1.4v3.3c0 .6.3 1.1.7 1.5.4.4 1 .5 1.6.4l1.9-.3 4.5-.7a2 2 0 0 0 1.6-2v-4c2.1-.6 4.1-1.4 6.1-2.3-1.1 4.7-5 12-17.8 12z"/><path fill="#FF0" d="m31.4 54.6 12.4 2.8h.4a2 2 0 0 0 2-2l-.2-.8-3.5-12.2c-.2-.7-.8-1.2-1.5-1.4-.7-.2-1.4.1-1.9.6l-8.9 9.8c-.5.5-.6 1.3-.4 2s.9 1 1.6 1.2zm23 2.8h.4l12.4-2.8c.7-.2 1.3-.7 1.5-1.3s.1-1.4-.4-2l-8.9-9.8c-.5-.5-1.2-.8-1.9-.6-.7.2-1.3.7-1.5 1.4l-3.5 12.5c-.2.7 0 1.4.5 1.9.3.4.8.7 1.4.7z"/></svg>""",
    "bat" : """<svg x="{1}" y="{2}" width="{0}" height="{0}" viewBox="7 -285 1038 1038"><path d="M509 407c-19-19-106-26-116-14-17 19-34 36-12-2-25 26-21 10 4-20 0 0 29-7 24-25-6-19-93-69-163-56-82 14-50 15-76-19-9-12-15-25-92-18-8-43-16-73-70-87C160 66 215 67 214 61c-3-31-14-66 10-4-1-54-4-38 10 2 3 9 69 40 123 51 75 16 98 33 98 22 0-8-7-30-13-34-15-8-27-71-9-85 5-4 95 66 95 66s81-66 90-70c12 10 17 50-9 88-6 7-9 24-9 31 0 15 130-12 209-62 25-16 12-69 19-13 17-48 13-29 6 6-2 7 112 23 210 122-24 0-60 4-67 73-70-1-78-2-107 42-80-6-155-9-191 22l-38 35 29 24c16 14 30 34 0 11 4 44 4 21-17-3-31 0-101 5-107 24-22 67-22 64-37-2z"/></svg>""",
}
