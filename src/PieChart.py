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

import math

_headerTemplate = '<svg viewBox="0 0 {0} {0}" width="{0}" height="{0}">'
_pathTemplate = '<path fill-rule="evenodd" fill="{0}" d="M {1},{2} A {3} {3} 0 {4} {5} {6} {7} L {3},{3} Z"/>'
_circleTemplate = '<circle fill="{0}" cx="{1}" cy="{1}" r="{1}"/>'
_animationTemplate = '<animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 {0} {0}" to="360 {0} {0}" dur="{1}s" repeatCount="indefinite"/>'

def svgPieChart(wedges, radius, animate, speed, includeSVGHeader=False) :
    """Generates an SVG of a pie chart. The intention is to include
    as part of a larger SVG (e.g., it does not insert xmlns into the
    opening svg tag). If wedges list is empty, it retrurns None.

    Keyword argument:
    wedges - A list of Python dictionaries, with each dictionary
        containing fields color and percentage.
    radius - the radius, in pixels for the pie chart.
    animate - Pass True to animate the pie chart.
    speed - If animate is True, then this input is the number of seconds for one full rotation.
    """
    if includeSVGHeader :
        components = [_headerTemplate.format(str(2*radius))]
    else :
        components = []

    if len(wedges) == 0 :
        return None
    elif len(wedges) == 1 :
        components.append(_circleTemplate.format(wedges[0]["color"], str(radius)))
    else :
        startPercentage = 0
        for w in wedges :
            endPercentage = startPercentage + w["percentage"]
            w["start"] = startPercentage * 2 * math.pi
            w["end"] = endPercentage * 2 * math.pi
            startPercentage = endPercentage
        # Adjustment for any possible rounding error that
        # may have occurred when initial percentages were computed
        # (i.e., last edge should complete a full circle).
        wedges[-1]["end"] = 2 * math.pi

        if animate :
            components.append("<g>")
            
        for w in wedges :
            components.append(
                _pathTemplate.format(
                    w["color"],
                    radius + radius * math.cos(w["start"]+math.pi),
                    radius + radius * math.sin(w["start"]+math.pi),
                    radius,
                    1 if w["percentage"] >= 0.5 else 0, # large arc flag
                    1, # clockwise=1
                    radius + radius * math.cos(w["end"]+math.pi),
                    radius + radius * math.sin(w["end"]+math.pi)
                    )
                )

        if animate :
            components.append(
                _animationTemplate.format(
                    radius,
                    speed
                    )
                )
            components.append("</g>")

    if includeSVGHeader :
        components.append("</svg>")
    return "".join(components)
