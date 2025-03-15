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

        #container for title and subtitle
        html.Div([
            html.H1("GLOBAL EV CHARGING INFRASTRUCTURE", style={
                'textAlign': 'center',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '48px',
                'padding': '5px',
            }),

            html.P("Visualizing location and features of electric vehicle charging infrastructure in 15 cities, with key summary statistics of important manufacturer information.", style={
                'textAlign': 'center',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '16px',
                'color': 'rgb(100, 100, 100)',
            })
        ], style={
            'backgroundColor': 'rgb(230, 230, 230)',  
            'textAlign': 'center',
            'fontFamily': 'Arial, sans-serif',
            'padding': '20px',  
            'marginBottom': '50px'  
        }),

        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
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


                    ]),
                    style={'backgroundColor': 'rgb(230, 230, 230)', 'marginBottom': '50px'}
                ),

                #displays how data is being filtered
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Applied Filters", style={'margin-top': '10px'}),
                        html.Div(id='filter-display', style={'fontSize': '16px', 'color': 'black', 'marginTop': '10px', 'marginBottom': '10px'}),

                    ]),
                    style={'backgroundColor': 'rgb(230, 230, 230)', 'marginBottom': '50px'}
                ),
                
                dbc.Row([
                    dbc.Col([
                        #table for average cost
                        dash_table.DataTable(
                            id='avg-cost-table',
                            columns=[
                                {"name": "Average Cost (USD/kWh)", "id": "Average Cost (USD/kWh)"}
                            ],
                            data=[{'Average Cost (USD/kWh)': 0}],
                            style_cell={'height': '50px','padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                            style_table={'height': 'auto', 'marginBottom': '30px'}, 
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}, #format the header with background color and bold font
                        ),
                        
                        # Table for average parking spots
                        dash_table.DataTable(
                            id='avg-parking-table',
                            columns=[
                                {"name": "Average Parking Spots", "id": "Average Parking Spots"}
                            ],
                            data=[{'Average Parking Spots': 0}],
                            style_cell={'height': '50px','padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                            style_table={'height': 'auto', 'overflowY': 'auto'},
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
                        ),
                    ]),

                    dbc.Col([
                         # Table for average reviews (ratings)
                        dash_table.DataTable(
                            id='avg-reviews-table',
                            columns=[
                                {"name": "Average Reviews (Rating)", "id": "Average Reviews (Rating)"}
                            ],
                            data=[{'Average Reviews (Rating)': 0}],
                            style_cell={'height': '50px','padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                            style_table={'height': 'auto', 'marginBottom': '30px'}, 
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                        ),

                        #table for total chargers
                        dash_table.DataTable(
                            id='total-chargers-table',
                            columns=[
                                {"name": "Total Chargers", "id": "Total Chargers"}
                            ],
                            data=[{'Total Chargers': 0}],
                            style_cell={'height': '50px','padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                            style_table={'height': 'auto', 'overflowY': 'auto'}, 
                            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                        ),

                    ]),

                ]),            
            ], md=4, style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),


            dbc.Col([
                #Map of world
                dcc.Graph(
                    id='map',
                    config={'scrollZoom': True},
                    style={'height': '54vh','width': '100%', 'marginBottom': '30px'}
                ),
                #Table for Hover data
                dash_table.DataTable(
                    id='table',
                    columns=[
                        {"name": "Station ID", "id": "Station ID"},
                        {"name": "Address", "id": "Address"},
                        {"name": "Charger Type", "id": "Charger Type"},
                        {"name": "Availability", "id": "Availability"},
                        {"name": "Cost (USD/kWh)", "id": "Cost (USD/kWh)"},
                        {"name": "Avg Users/day", "id": "Usage Stats (avg users/day)"},
                        {"name": "Parking Spots", "id": "Parking Spots"}
                    ],
                    data=ev[['Station ID', 'Address', 'Charger Type', 'Availability', 'Cost (USD/kWh)', 'Parking Spots']].to_dict('records'),
                    page_size=1,
                    style_cell={'height': '40px', 'padding': '5px', 'fontFamily': 'Arial, sans-serif'},
                    style_table={'height': 'auto', 'overflowY': 'auto'}, 
                    style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'}],
                     style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',

                    },
                ),
            ], md=8, style={'backgroundColor': '#BCD4E6'}),
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
    Output('total-chargers-table', 'data'),
    Output('filter-display', 'children')],
    [Input('charger-type-dropdown', 'value'),
    Input('crossfilter-year-slider', 'value'),
    Input('map', 'relayoutData')]
)

def update_map_table(charger_type, year_range, relayoutData):

    #default values for zoom and positioning of map
    zoom = 1
    center = {'lat': 0, 'lon': 0}

    #prevents map from resetting each time filter is apllied
    if relayoutData is not None:
        zoom = relayoutData.get('mapbox.zoom', zoom)  
        center = relayoutData.get('mapbox.center', center) 

    filtered_ev = ev.copy()

    #filter data by installation year based on slider selection
    filtered_ev = filtered_ev[(filtered_ev["Installation Year"] >= year_range[0]) & (filtered_ev["Installation Year"] <= year_range[1])]
    
    #filter data by charger type based on dropdown selection
    if charger_type != 'All':
        filtered_ev = filtered_ev[filtered_ev['Charger Type'] == charger_type]

    #different colors for charger type
    charger_type_colors = {
        'AC Level 1': 'green',
        'AC Level 2': 'red',
        'DC Fast Charger': 'blue'
    }

    fig = go.Figure()

    #create map based off filtering
    fig.add_trace(go.Scattermapbox(
        lat=filtered_ev["Latitude"],
        lon=filtered_ev["Longitude"],
        mode='markers+text',
        text=filtered_ev['Station ID'],
        marker={'size': 10, 'color': filtered_ev['Charger Type'].map(charger_type_colors)}
        
    ))
    
    fig.update_layout(
        margin=dict(
        l=20,  
        r=20,  
        t=20,  
        b=20   
        ),
        paper_bgcolor="rgb(230, 230, 230)",
        mapbox_style="open-street-map",  
        mapbox=dict(
            accesstoken="AIzaSyDmLCWxhqJteqUEpSStBLKm2r4oQPfHg4o",
            center=center,
            zoom=zoom,
    ),
    )

    # Calculate the average cost
    avg_cost = filtered_ev["Cost (USD/kWh)"].mean() if not filtered_ev.empty else 0
    avg_cost_data = [{'Average Cost (USD/kWh)': round(avg_cost, 4)}]

    # Calculate the average parking spots
    avg_parking_spots = filtered_ev["Parking Spots"].mean() if not filtered_ev.empty else 0
    avg_parking_data = [{'Average Parking Spots': round(avg_parking_spots, 1)}]

    # Calculate the average reviews rating
    avg_reviews = filtered_ev["Reviews (Rating)"].mean() if not filtered_ev.empty else 0
    avg_reviews_data = [{'Average Reviews (Rating)': round(avg_reviews, 2)}]

    #calculate total chargers
    total_chargers = filtered_ev.shape[0] if not filtered_ev.empty else 0
    total_chargers_data = [{'Total Chargers': total_chargers}]

    # Text to display applied filters
    filter_text = f"Charger Type: {charger_type}, Year Range: {year_range[0]} - {year_range[1]}"

    return fig, avg_cost_data, avg_parking_data, avg_reviews_data, total_chargers_data, filter_text

# Callback to update table based on map hover
@app.callback(
    Output('table', 'data'),
    Input('map', 'hoverData')
)
def update_table_on_hover(hoverData):
    if hoverData is None:
        return ev[['Station ID', 
                   'Address', 
                   'Charger Type', 
                   'Availability', 
                   'Cost (USD/kWh)', 
                   'Parking Spots', 
                   'Usage Stats (avg users/day)', 
                   'Connector Types']].to_dict('records')
    
    # Extract the Station ID from hoverData
    station_id = hoverData['points'][0]['text']
    
    # Filter the data to show only the row corresponding to the hovered station
    filtered_data = ev[ev['Station ID'] == station_id][['Station ID', 
                                                        'Address', 
                                                        'Charger Type', 
                                                        'Availability', 
                                                        'Cost (USD/kWh)', 
                                                        'Parking Spots', 
                                                        'Usage Stats (avg users/day)', 
                                                        'Connector Types']]
    
    return filtered_data.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)