from turtle import *
from math import *
from plotly import graph_objects as go
import numpy as np
import streamlit as st
from fractions import Fraction

# '''
# How many rotations?
#     smaller number of the reduced ratio of the circle circumferences
#     if R is the number of teeth in the outer circle
#     and r is the number of teeth in the inner circle
#     the number of rotations is the smaller number of the reduced fraction
#     R/r
#     example
#     R = 24
#     r = 13
#     R/r can't be reduced so it will take 13 rotations
#
#
# What is the path?
#     let's start with the original point of contact
#
#     R = outer radius
#     r = inner radius
#
#     theta = angle of rotation of the origin relative to the outer circle
#     alpha = angle of rotation of the origin relative to the inner circle
#
#     R * theta = arc lenth of travel (same for both inner and outer circle)
#         arc lenth of rolling must be the same
#
#     We can calculate angle of the arc of travel on the inner circle as
#     (R/r) * theta
#
#     we can see that one trip around the smaller circle is (tau) =
#     (R/r)* theta + alpha - theta
#     so alpha = tau - ((R/r) - 1) * theta
#     (subtracting tau makes the same angle since tau is 360 degrees)
#     alpha = -((R/r) -1) * theta
#
#     We know that location of the CENTER of the small circle is always
#     x = (R-r)*cos(theta)
#     y = (R-r)*sin(theta)
#
#     to compensate for the fact that the pen is moving around the outer part of the smaller
#     circle we need to add the movement of the outer circle which is
#
#     x = r*cos(alpha)
#     y = r*sin(alpha)
#
#     we can sub in the formula for alpha:
#
#     x = r*cos(-((R/r) -1) * theta)
#     y = r*sin(-((R/r) -1) * theta)
#
#
#     we can simplify this into
#     x = r*cos(((R/r) -1) * theta)  (cos is an even function so the negative doesn't matter)
#     y = -r*sin(((R/r) -1) * theta) (sin is an odd function so we can move the - out front)
#
#     okay, so at this point we have the following equation to get the point of origin
#     on the inner circle:
#
#     x = (R-r)*cos(theta) + r*cos(((R/r) -1) * theta)
#     y = (R-r)*sin(theta) - r*sin(((R/r) -1) * theta)
#
#     but this assumes that the pen is always on the outer edge of the inner circle,
#     which it's not.  so we need to modify r but only on the part where we are
#     adding the bit for the inner movement.  if we use p to indicate the offset of the pen
#     from the center of the inner circle the r for the pen is:
#
#     (r*p)
#
#     if p = 1 (or 100%) the pen radius is the same as the full inner radius
#
#     so finally we have:
#
#     x = (R-r)*cos(theta) + r*cos(((R/(r*p)) -1) * theta)
#     y = (R-r)*sin(theta) - r*sin(((R/(r*p)) -1) * theta)
#
#     If we normalize R to 1 we can determine the value of theta to be
#     between 0 and

# '''



def formulaX(M, N, p, t):
    x1 = (1-(N/M))*cos(N*t)
    x2 = (N/M)*cos((M-N)*(t))
    x = x1 + p * x2
    return x

def formulaY(M, N, p, t):
    y1 = (1-(N/M))*sin(N*t)
    y2 = (N/M)*sin((M-N)*(t))
    y = y1 + p * y2
    return y

def plot_spiro(M, N, p, color, num_points):
    # todo calculate actual value for theta
    min_num = min(M, N)
    t = np.linspace(start = 0, stop=2*min_num*pi, num = num_points, endpoint = True)
    t = [x.round(4) for x in t] #rounding to avoid near miss overlap
    t[-1] = 2*min_num*pi
    x = [formulaX(M, N, p, a) for a in t]
    y = [formulaY(M, N, p, a) for a in t]
    return go.Scatter(x = x, y = y,  mode="lines", line = dict(color=color, width=1))


def main():
    st.set_page_config(layout="wide")
    if 'traces' not in st.session_state:
        st.session_state['traces'] = []

    coll, colr = st.columns([1, 3])

    col1A, col2A = coll.columns([3, 1])


    R = col1A.slider('Outer Radius', 1, 100)
    r = col1A.slider('Inner Radius', 1, 100)
    p = col1A.slider('Pen offset', .1, 1.0, step = .001)
    num_points = col1A.slider('points', 100, 10000, step=100)


    a = Fraction(R, r)
    N = a.denominator
    M = a.numerator


    color = col2A.color_picker('Pick A Color', '#00f900', key = "trace_color")
    bgcolor = col2A.color_picker('Background color', '#F6F7F6', key = "bgcolor")

    temp_trace = plot_spiro(M, N, p, color, num_points)
    if col1A.button('add to image'):
        st.session_state.traces.append(temp_trace)
    if col1A.button('Reset Image'):
        st.session_state.traces = []

    temp_container = coll.container()
    image_container = colr.container()

    temp_fig = go.Figure()
    temp_fig.add_trace(temp_trace)


    temp_fig.update_layout(xaxis=dict(showgrid=False,
                                      zeroline=False,
                                      showticklabels=False),
                          yaxis=dict(showgrid=False,
                                     zeroline=False,
                                     showticklabels=False,
                                     scaleanchor="x",
                                     scaleratio=1,
                                     ),
                           plot_bgcolor='black'
                           )
    temp_container.plotly_chart(temp_fig, use_container_width=True)


    fig = go.Figure()
    for t in st.session_state['traces']:
        fig.add_trace(t)

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=  1,
    )
    fig.update_layout(height = 800,
                      xaxis=dict(showgrid=False,
                                 zeroline=False,
                                 showticklabels=False,),
                      yaxis=dict(showgrid=False,
                                 zeroline=False,
                                 showticklabels=False,
                                     scaleanchor="x",
                                     scaleratio=1,
                                     ),
                      plot_bgcolor=bgcolor
                      )
    image_container.plotly_chart(fig, use_container_width=True)

main()
