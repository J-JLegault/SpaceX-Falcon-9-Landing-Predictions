#Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
from dash import html

#import dash_core_components as dcc
from dash import dcc

from dash.dependencies import Input, Output
import plotly.express as plotEx

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

#spacex_df = spacex_df['Class'].replace('0', 'Failed')
#spacex_df = spacex_df['Class'].replace('1', 'Success')

min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children = [html.H1('SpaceX Launch Records Dashboard',
                                          style = {'textAlign': 'center', 
                                                   'font-color': '#000000', 
                                                   'font-family': 'Arial', 
                                                   'font-size': 40}),

                                  # TASK 1: Add a dropdown list to enable Launch Site selection
                                  # ---------------------------------------------------------------------------------------------------------------
                                  # Dropdown List
                                  # ---------------------------------------------------------------------------------------------------------------
                                  dcc.Dropdown(id = 'site-dropdown',
                                               options = [
                                                          {'label': 'All Sites', 'value': 'ALL'},
                                                          {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                          {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                          {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                          {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                         ],
                                               value = 'ALL',
                                               placeholder = "Select a Launch Site", 
                                               searchable = True,
                                               style = {'font-size': '18px',
                                                        'font-color': '#3333cc',
                                                        'font-family': 'Arial'}),
                                  # ---------------------------------------------------------------------------------------------------------------
                                  
                                  html.Br(),

                                  # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                  # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                  html.Div(dcc.Graph(id = 'success-pie-chart')),
                                  
                                  html.Br(),

                                  html.P('Payload range (Kg):', 
                                         style = {'font-size': '18px',
                                                  'font-color': '#3333cc',
                                                  'font-family': 'Arial'}),

                                  # TASK 3: Add a slider to select payload range
                                  # ---------------------------------------------------------------------------------------------------------------
                                  # Range Slider
                                  # ---------------------------------------------------------------------------------------------------------------
                                  dcc.RangeSlider(id = 'payload-slider',
                                                  min = 0,
                                                  max = 10000, 
                                                  step = 1000,
                                                  value = [min_payload, max_payload],
                                                  marks = {'0': {'label': '0', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}}, 
                                                           '1000': {'label': '1000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '2000': {'label': '2000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '3000': {'label': '3000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '4000': {'label': '4000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '5000': {'label': '5000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '6000': {'label': '6000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '7000': {'label': '7000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '8000': {'label': '8000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '9000': {'label': '9000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}},
                                                           '10000': {'label': '10000', 'style': {'color': '#000000', 'font-family': 'Arial', 'font-size': 16}}}, 
                                                 ),
                                  # ---------------------------------------------------------------------------------------------------------------

                                  # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                  html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
                                 ])

# TASK 2:
# ---------------------------------------------------------------------------------------------------------------
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# ---------------------------------------------------------------------------------------------------------------
@app.callback(
        Output(component_id = 'success-pie-chart', component_property = 'figure'),
        Input(component_id = 'site-dropdown', component_property = 'value'))

def build_graph(site_dropdown):
    if site_dropdown == 'ALL':
        piechart = plotEx.pie(data_frame = spacex_df, names = 'Launch Site', values = 'Class', title = 'Total Launches for All Sites')
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        specific_site = 'Total Launch for Site ' + site_dropdown
        piechart = plotEx.pie(data_frame = specific_df, names = 'Class', title = specific_site)

    piechart.update_layout(
        font_family = "Arial",
        font_color = "#000000",
        font_size = 16,

        title_font_family = "Arial",
        title_font_color = "#3333cc",
        title_font_size = 20,

        legend_title_font_family = "Arial",
        legend_title_font_color = "#3333cc",
        legend_title_font_size = 16
    )

    return piechart
# ---------------------------------------------------------------------------------------------------------------

# TASK 4:
# ---------------------------------------------------------------------------------------------------------------
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# ---------------------------------------------------------------------------------------------------------------
@app.callback(
        Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
        [Input(component_id = 'site-dropdown', component_property = 'value'),
        Input(component_id = 'payload-slider', component_property = 'value')])

def update_graph(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_slider[0]) 
        & (spacex_df['Payload Mass (kg)'] <= payload_slider[1])]
        scatterplot = plotEx.scatter(data_frame = filtered_data, x = "Payload Mass (kg)", y = "Class", 
        color = "Booster Version Category")
    else:
        specific_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        filtered_data = specific_df[(specific_df['Payload Mass (kg)'] >= payload_slider[0]) 
        & (spacex_df['Payload Mass (kg)'] <= payload_slider[1])]
        scatterplot = plotEx.scatter(data_frame = filtered_data, x = "Payload Mass (kg)", y = "Class", 
        color = "Booster Version Category")

    scatterplot.update_layout(
        font_family = "Arial",
        font_color = "#000000",
        font_size = 16,

        title_text = "Correlation between Payload and Success Rate for all Sites",
        title_font_family = "Arial",
        title_font_color = "#3333cc",
        title_font_size = 20,

        legend_title_font_family = "Arial",
        legend_title_font_color = "#3333cc",
        legend_title_font_size = 16
    )

    scatterplot.update_xaxes(title_font_family = "Arial", 
                             title_font_color = "#3333cc",
                             title_font_size = 20)

    scatterplot.update_yaxes(title_font_family = "Arial", 
                             title_font_color = "#3333cc",
                             title_font_size = 20)

    return scatterplot
# ---------------------------------------------------------------------------------------------------------------

# Run the app
if __name__ == '__main__':
    app.run_server()
