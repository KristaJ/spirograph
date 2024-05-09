from turtle import *
from math import *
from plotly import graph_objects as go
import numpy as np
import streamlit as st


def formulaX(R, r, p, t):
    x = (R-r)*cos(t) - (r + p)*cos((R-r)/r*t)
    x = (R-r) * cos(t)
    x = x-(r + p)*cos((R-r)/r*t)
    return x

def formulaY(R, r, p, t):
    y = (R-r)*sin(t) - (r + p)*sin((R-r)/r*t)
    y = (R-r) * sin(t)
    y = y-(r + p)*sin((R-r)/r*t)
    return y

def plot_spiro(R, r, p, color):
    # todo calculate actual value for theta
    theta = np.linspace(pi, 10*pi, 4000)
    x = [formulaX(R, r, p, t) for t in theta]
    y = [formulaY(R, r, p, t) for t in theta]
    return go.Scatter(x = x, y = y,  line = dict(color=color, width=1))


def main():
    st.set_page_config(layout="wide")
    if 'traces' not in st.session_state:
        st.session_state['traces'] = []

    coll, colr = st.columns([1, 3])

    col1A, col2A = coll.columns([3, 1])


    R = col1A.slider('Outer Radius', 1, 500)
    r = col1A.slider('Inner Radius', 1, 100)
    p = col1A.slider('Pen offset', 1, 100)

    color = col2A.color_picker('Pick A Color', '#00f900', key = "trace_color")
    bgcolor = col2A.color_picker('Pick A Color', '#F6F7F6', key = "bgcolor")

    temp_trace = plot_spiro(R, r, p, color)
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
