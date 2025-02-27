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

    #container for everything
    html.Div([

        #container for dropdown and slider
        html.Div([

            #dropdown for charger type
            dcc.Dropdown(
                id='charger-type-dropdown',
                options=[
                    {'label': 'AC Level 1', 'value': 'AC Level 1'},
                    {'label': 'AC Level 2', 'value': 'AC Level 2'},
                    {'label': 'DC Fast Charger', 'value': 'DC Fast Charger'},
                    {'label': 'Show All Chargers', 'value': 'All'}
                ],
                value='All',
                style={'width': '100%', 'display': 'inline-block'}
            ), 

            #slider based on installation year
            dcc.Slider(
                id='crossfilter-year-slider',
                min=ev["Installation Year"].min(),
                max=ev["Installation Year"].max(),
                step=1,
                value=ev['Installation Year'].max(),
                marks={str(year): str(year) for year in sorted(ev["Installation Year"].unique())},
                tooltip={"placement": "bottom", "style": {"width": '50%'}, "always_visible": True}
            ),
        ], style={'width': '40%', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'left'}),



        #container for graph
        html.Div([
            dcc.Graph(
                id='map',
                config={'scrollZoom': True}
            ),
        ], style={'width': '60%'}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start', 'width': '100%'}),
], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '100%'}
)

#callback to update map
@app.callback(
    Output('map', 'figure'),
    Input('charger-type-dropdown', 'value'),
    Input('crossfilter-year-slider', 'value'),
    [Input('map', 'relayoutData')]
)

def update_map(charger_type, year_value, relayoutData):

#default values for zoom and positioning of map
    zoom = 1
    center = {'lat': 0, 'lon': 0}

    if relayoutData is not None:
        zoom = relayoutData.get('mapbox.zoom', zoom)  
        center = relayoutData.get('mapbox.center', center) 

    filtered_ev = ev.copy()

    fig = go.Figure()

    #filter data by installation year based on slider selection
    filtered_ev = filtered_ev[filtered_ev["Installation Year"] == year_value]
    
    #filter data by charger type based on dropdown selection
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