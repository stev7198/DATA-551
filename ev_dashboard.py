from dash import Dash, html
from dash import dcc
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

#read data and remove stations that have Random Rd
ev = pd.read_csv("ev_charging_stations.csv")
ev = ev[~ev['Address'].str.contains('Random Rd', case=False)]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Container([
        #Main Title
        html.H1("EV Chargers Around the World", style={
            'textAlign': 'center',
            'fontFamily': 'Arial, sans-serif', #specify a font
            'marginTop': '30px' #add spacing for cleaner look
            }),

        dbc.Row([
            dbc.Col([
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
                    style={
                        'width': '100%',
                        'display': 'inline-block',
                        'borderRadius': '5px', #Round the borders of dropdown menu
                    }
                ), 

                #slider based on installation year
                html.H5("Select Installation Year", style={
                    'marginTop': '20px',
                    
                }),
                html.Div(
                    dcc.RangeSlider(
                        id='crossfilter-year-slider',
                        min=ev["Installation Year"].min(),
                        max=ev["Installation Year"].max(),
                        step=1,
                        value=[ev["Installation Year"].min(), ev['Installation Year'].max()],
                        marks={str(year): str(year) for year in sorted(ev["Installation Year"].unique())},
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    style={'marginTop': '20px'}
                ),


                #Displays how the data is being filtered
                html.H4("Applied Filters", style={'margin-top': '20px'}),
                html.Div(id='filter-display', style={'fontSize': '16px', 'color': 'black', 'marginTop': '10px'}),
                
                 # Table for average cost
                html.H4("Average Cost (USD/kWh)", style={'margin-top': '20px'}),
                dash_table.DataTable(
                    id='avg-cost-table',
                    columns=[
                        {"name": "Average Cost (USD/kWh)", "id": "Average Cost (USD/kWh)"}
                    ],
                    data=[{'Average Cost (USD/kWh)': 0}],
                    style_cell={'padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                    style_table={'height': 'auto', 'overflowY': 'auto'}, 
                    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}, #format the header with background color and bold font
                ),

                # Table for average parking spots
                html.H4("Average Parking Spots", style={'margin-top': '20px'}),
                dash_table.DataTable(
                    id='avg-parking-table',
                    columns=[
                        {"name": "Average Parking Spots", "id": "Average Parking Spots"}
                    ],
                    data=[{'Average Parking Spots': 0}],
                    style_cell={'padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                    style_table={'height': 'auto', 'overflowY': 'auto'},
                    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                ),

                # Table for average reviews (ratings)
                html.H4("Average Reviews (Rating)", style={'margin-top': '20px'}),
                dash_table.DataTable(
                    id='avg-reviews-table',
                    columns=[
                        {"name": "Average Reviews (Rating)", "id": "Average Reviews (Rating)"}
                    ],
                    data=[{'Average Reviews (Rating)': 0}],
                    style_cell={'padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                    style_table={'height': 'auto', 'overflowY': 'auto'}, 
                    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                ),
                
            ], md=4, style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),


            dbc.Col([
                #Map of world
                dcc.Graph(
                    id='map',
                    config={'scrollZoom': True},
                    style={'height': '70vh','width': '100%'}
                ),
                #Table for Hover data
                dash_table.DataTable(
                    id='table',
                    columns=[
                        {"name": "Station ID", "id": "Station ID"},
                        {"name": "Address", "id": "Address"},
                        {"name": "Charger Type", "id": "Charger Type"},
                        {"name": "Availability", "id": "Availability"},
                        {"name": "Cost (USD/kWh)", "id": "Cost (USD/kWh)"}
                    ],
                    data=ev[['Station ID', 'Address', 'Charger Type', 'Availability', 'Cost (USD/kWh)']].to_dict('records'),
                    page_size=1,
                    style_cell={'padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                    style_table={'height': 'auto', 'overflowY': 'auto'}, 
                    style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'}],
                     style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                ),
            ], md=8, style={'backgroundColor': 'lightgrey'}),
        ]),
    ], fluid=True),
],
style={
    'backgroundColor': '#BCD4E6',
    'minHeight': '100vh'
})

#callback to update map
@app.callback(
    [Output('map', 'figure'),
    Output('avg-cost-table', 'data'),
    Output('avg-parking-table', 'data'),
    Output('avg-reviews-table', 'data'),
    Output('filter-display', 'children')],
    [Input('charger-type-dropdown', 'value'),
    Input('crossfilter-year-slider', 'value'),
    Input('map', 'relayoutData')]
)

def update_map_table(charger_type, year_range, relayoutData):

    #default values for zoom and positioning of map
    zoom = 1
    center = {'lat': 0, 'lon': 0}

    if relayoutData is not None:
        zoom = relayoutData.get('mapbox.zoom', zoom)  
        center = relayoutData.get('mapbox.center', center) 

    filtered_ev = ev.copy()


    #filter data by installation year based on slider selection
    filtered_ev = filtered_ev[(filtered_ev["Installation Year"] >= year_range[0]) & (filtered_ev["Installation Year"] <= year_range[1])]
    
    #filter data by charger type based on dropdown selection
    if charger_type != 'All':
        filtered_ev = filtered_ev[filtered_ev['Charger Type'] == charger_type]


    fig = go.Figure()

    #create map based off filtering
    fig.add_trace(go.Scattermapbox(
        lat=filtered_ev["Latitude"],
        lon=filtered_ev["Longitude"],
        mode='markers+text',
        text=filtered_ev['Station ID'],
        marker={'size': 10, 'color': 'blue'}
        
    ))
    
    fig.update_layout(
        mapbox_style="open-street-map",  
        mapbox=dict(
            accesstoken="AIzaSyDmLCWxhqJteqUEpSStBLKm2r4oQPfHg4o",
            center=center,
            zoom=zoom,
    ),
    )

    # Calculate the average cost
    avg_cost = filtered_ev["Cost (USD/kWh)"].mean() if not filtered_ev.empty else 0
    avg_cost_data = [{'Average Cost (USD/kWh)': avg_cost}]

    # Calculate the average parking spots
    avg_parking_spots = filtered_ev["Parking Spots"].mean() if not filtered_ev.empty else 0
    avg_parking_data = [{'Average Parking Spots': avg_parking_spots}]

    # Calculate the average reviews rating
    avg_reviews = filtered_ev["Reviews (Rating)"].mean() if not filtered_ev.empty else 0
    avg_reviews_data = [{'Average Reviews (Rating)': avg_reviews}]

    # Text to display applied filters
    filter_text = f"Charger Type: {charger_type}, Year Range: {year_range[0]} - {year_range[1]}"

    return fig, avg_cost_data, avg_parking_data, avg_reviews_data, filter_text

# Callback to update table based on map hover
@app.callback(
    Output('table', 'data'),
    Input('map', 'hoverData')
)
def update_table_on_hover(hoverData):
    if hoverData is None:
        return ev[['Station ID', 'Address', 'Charger Type', 'Availability', 'Cost (USD/kWh)']].to_dict('records')
    
    # Extract the Station ID from hoverData
    station_id = hoverData['points'][0]['text']
    
    # Filter the data to show only the row corresponding to the hovered station
    filtered_data = ev[ev['Station ID'] == station_id][['Station ID', 'Address', 'Charger Type', 'Availability', 'Cost (USD/kWh)']]
    
    return filtered_data.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)