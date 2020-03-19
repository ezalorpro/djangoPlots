from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go

import numpy as np

# Create your views here.

def home(request):
    x_data = np.linspace(0, 2*np.pi, 300)
    y_data = np.sin(x_data)
    
    trace = go.Scatter(x=x_data, y=y_data,
                       mode='lines', name='sin',
                       opacity=0.8, marker_color='blue')
    data = [trace]
    layout = go.Layout(
        margin=dict(l=10, r=20, t=40, b=20),
        xaxis=dict(autorange=True),
        yaxis=dict(autorange=True)
    )
    
    fig = go.Figure(data=data, layout=layout)
    
    plot_div = plot(fig, output_type='div', include_plotlyjs=True, show_link=False)
    return render(request, 'plots/home.html', {'plot_div': plot_div})
