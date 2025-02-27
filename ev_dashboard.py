from dash import Dash, html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

#read data and remove stations that have Random Rd
ev = pd.read_csv("ev_charging_stations.csv")
ev = ev[~ev['Address'].str.contains('Random Rd', case=False)]

app = Dash()

app.layout = html.Div([
    html.H1("EV Chargers Around the World", style={'textAlign': 'center'}),

    html.Div([

#dropdown menu for charger type
    dcc.Dropdown(
        id='charger-type-dropdown',
        options=[
            {'label': 'AC Level 1', 'value': 'AC Level 1'},
            {'label': 'AC Level 2', 'value': 'AC Level 2'},
            {'label': 'DC Fast Charger', 'value': 'DC Fast Charger'},
            {'label': 'Show All Chargers', 'value': 'All'}
        ],
        value='All',
        style={'width': '48%', 'display': 'inline-block'}
    ),

    dcc.Graph(
        id='map',
        config={'scrollZoom': True}
    )
],
style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'}),
])

#callback to update map
@app.callback(
    Output('map', 'figure'),
    Input('charger-type-dropdown', 'value'),
    [Input('map', 'relayoutData')]
)

def update_map(charger_type, relayoutData):

#default values for zoom and positioning of map
    zoom = 1
    center = {'lat': 0, 'lon': 0}

    if relayoutData is not None:
        zoom = relayoutData.get('mapbox.zoom', zoom)  
        center = relayoutData.get('mapbox.center', center) 

    filtered_ev = ev.copy()

    fig = go.Figure()

#filter data type based on dropdown selection
    if charger_type != 'All':
        filtered_ev = filtered_ev[filtered_ev['Charger Type'] == charger_type]

#create map based off filtering
    fig.add_trace(go.Scattermapbox(
        lat=filtered_ev["Latitude"],
        lon=filtered_ev["Longitude"],
        mode='markers+text',
        text=filtered_ev['Station ID'],
        marker={'size': 10, 'color': 'red'}
        
    ))
    
    fig.update_layout(
        mapbox_style="open-street-map",  
        mapbox=dict(
            accesstoken="AIzaSyDmLCWxhqJteqUEpSStBLKm2r4oQPfHg4o",
            center=center,
            zoom=zoom,
    ),
    )

    return fig 

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)