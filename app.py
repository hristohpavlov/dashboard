import numpy as np
import pandas as pd
from pandas.core.indexes import multi
import plotly.express as px
import matplotlib.pyplot as plt

import dash
import os

here = os.path.dirname(os.path.abspath(__file__))
from dash import dcc,html
from dash.dependencies import Input, Output

#Initialize dashboard application
app = dash.Dash(__name__)
server = app.server

# Data exploration and cleaning with pandas

# -----------------------------------------

# -----------------------------------------
#       Energy Generation by State
# -----------------------------------------
filename1 = os.path.join(here, 'annual_generation_state.xls')
filename2 = os.path.join(here, 'annual_consumption_total.xlsx')
df = pd.read_excel(filename1, header=1)
# print(df)
# print(df.columns)
# Clear state column
# Total Energy Generation
df_gen_total = df.copy()
df_gen_total['STATE'] = df_gen_total['STATE'].replace({'US-TOTAL':'US-Total'})
df_gen_total_final = df_gen_total[df_gen_total['STATE'] == 'US-Total']
# print(df_gen_total_final)

# Replace US-TOTAL with US-Total to combine in 1 category and replace empty cells with NaN
df['STATE'] = df['STATE'].replace({'US-TOTAL': np.nan,'US-Total': np.nan, '  ' : np.nan})
# Drop the NaN values in State cell
df= df.dropna(subset=['STATE'])
# print(df.STATE.unique())
# USA has 50 states, and we can check how many unique entries are in dataset. It shows 52 which means there is a duplicate state, since there is also US-Total.
# print(df['STATE'].nunique())
# After quick observation we can see that there is no state with code WA (Washington DC), it is DC, so change name accordingly
df['STATE'] = df['STATE'].replace({'WA' : 'DC'})
# Check if replacement has been successful
# print(df.STATE.unique())
# print(df.STATE.nunique())
# print(df['TYPE OF PRODUCER'].unique())

# -----------------------------------------
#       Total Energy Consumption
# -----------------------------------------
df_prod = pd.read_excel(filename2, sheet_name="Annual Data", header=10, dtype=object)
# print(df_prod.columns)
#Convert energy units from BTUs to MWh in excel with KuTools extension
#Current energy unit is Quadrillion MWh
#Remove years before 1990, to match the other dataset
df_prod = df_prod[df_prod['Annual Total'] > 1989]
df_prod = df_prod.reset_index()
# print(df_prod)

# Total Energy Consumption

df_cons_total = df_prod.copy()
df_cons_total = df_cons_total[{'Annual Total','Total Renewable Energy Consumption','Total Primary Energy Consumption'}]
df_cons_total['Total Energy Consumption'] = df_cons_total['Total Renewable Energy Consumption'] + df_cons_total['Total Primary Energy Consumption']
print(df_cons_total)
# ------------------------------------------

# Dashboard app layout

app.layout = html.Div([
    html.H1("Energy Generation and Consumption in the US", style={'text-align': 'center'}),
    html.Br(),
    html.Div([
    html.Div([
    html.Br(),
    dcc.Slider(id='year_slider',
    min=1990,
    max=2020,
    step=1,
    value=2020,
    updatemode='drag',
    marks={
        1990: '1990',
        1991: '1991',
        1992: '1992',
        1993: '1993',
        1994: '1994',
        1995: '1995',
        1996: '1996',
        1997: '1997',
        1998: '1998',
        1999: '1999',
        2000: '2000',
        2001: '2001',
        2002: '2002',
        2003: '2003',
        2004: '2004',
        2005: '2005',
        2006: '2006',
        2007: '2007',
        2008: '2008',
        2009: '2009',
        2010: '2010',
        2011: '2011',
        2012: '2012',
        2013: '2013',
        2014: '2014',
        2015: '2015',
        2016: '2016',
        2017: '2017',
        2018: '2018',
        2019: '2019',
        2020: '2020',
    }
    ),
    html.Br(),
    html.Div([
        html.Div([
        html.Label('Energy source'),
        dcc.Dropdown(id="slct_type",
            options=[
                {"label": "Total", "value": "Total"},
                {"label": "Coal", "value": "Coal"},
                {"label": "Hydroelectric Conventional", "value": "Hydroelectric Conventional"},
                {"label": "Natural Gas", "value": "Natural Gas"},
                {"label": "Petroleum", "value": "Petroleum"},
                {"label": "Wind", "value": "Wind"},
                {"label": "Wood and Wood Derived Fuels", "value": "Wood and Wood Derived Fuels"},
                {"label": "Nuclear", "value": "Nuclear"},
                {"label": "Other Biomass", "value": "Other Biomass"},
                {"label": "Other Gases", "value": "Other Gases"},
                {"label": "Pumped Storage", "value": "Pumped Storage"},
                {"label": "Geothermal", "value": "Geothermal"},
                {"label": "Other", "value": "Other"},
                {"label": "Solar Thermal and Photovoltaic", "value": "Solar Thermal and Photovoltaic"}],
                multi=False,
                value="Total",
                style={'width': '75%'}
        ),
    ], style={'width': '70%', 'float': 'left', 'margin-left': '80px'}),
    html.Div([
        html.Label('Type of energy producer'),
        dcc.Dropdown(id="slct_producer",
        options=[
            {"label": "Total Electric Power Industry", "value": "Total Electric Power Industry"},
            {"label": "Electric Generators, Electric Utilities", "value": "Electric Generators, Electric Utilities"},
            {"label": "Combined Heat and Power, Industrial Power", "value": "Combined Heat and Power, Industrial Power"},
            {"label": "Combined Heat and Power, Commercial Power", "value": "Combined Heat and Power, Commercial Power"},
            {"label": "Electric Generators, Independent Power Producers", "value": "Electric Generators, Independent Power Producers"},
            {"label": "Combined Heat and Power, Electric Power", "value": "Combined Heat and Power, Electric Power"}],
            multi=False,
            value="Total Electric Power Industry",
            style={'width': '75%'}
        ),
    ],style={'width':'70%','float':'right','margin-right':'-100px'}),
    ],style={'width':'100%','display':'flex'}),
    html.Br(),],style={'border-radius':'10px','background-color':'#CDCDCD', 'padding':'15px'}),
    html.Div([html.Div(id='output_container', children=[], style={'text-align': 'center','background-color':'#CDCDCD', 'padding':'15px', 'border-radius': '10px 10px 0px 0px'}),
    html.Br(),dcc.Graph(id='states_map', figure={})], style={'margin-top':'20px'}),
    ],style={'float':'left','width':'56.5%'}),
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='cons_by_source', figure={})
            ], style = {'width': '50%', 'float': 'left'}),
            html.Div([
                dcc.Graph(id='prod_by_source', figure={})
            ], style = {'width': '50%', 'float': 'right'}),
        ], style={'display':'flex'}),
        html.Div([
            html.Div([
                dcc.Graph(id='cons_by_year', figure={})
            ], style = {'width': '50%', 'float': 'left'}),
            html.Div([
                dcc.Graph(id='prod_by_year', figure={})
            ], style = {'width': '50%', 'float': 'right'}),
        ], style={'display':'flex'}),
    ],style={'float':'right','width': '40%','border-radius':'10px','background-color':'#CDCDCD', 'padding':'15px'})
],style={'width':'100%'})

# App Callback

# ---------------------------------------

@app.callback(
    [Output(component_id='states_map', component_property='figure'),
    Output(component_id='output_container', component_property='children'),
    Output(component_id='cons_by_source', component_property='figure'),
    Output(component_id='prod_by_source', component_property='figure'),
    Output(component_id='cons_by_year', component_property='figure'),
    Output(component_id='prod_by_year', component_property='figure')],
    [Input(component_id='year_slider', component_property='value'),
    Input(component_id='slct_type', component_property='value'),
    Input(component_id='slct_producer', component_property='value')]
)
def update_graph(value, source_value, producer_value):
    print(value)
    print(source_value)
    print(producer_value)
    container = 'Selected year: {}'.format(value)
    dff = df.copy()
    dff = dff[dff['YEAR'] == value]
    dff = dff[dff['ENERGY SOURCE'] == source_value]
    dff = dff[dff['TYPE OF PRODUCER'] == producer_value]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='GENERATION (Megawatthours)',
    )

    dff_cons_final = df_gen_total_final.copy()
    dff_cons_final = dff_cons_final[dff_cons_final['ENERGY SOURCE'] == source_value]
    fig2 = px.bar(data_frame= dff_cons_final, x='YEAR', y='GENERATION (Megawatthours)')

    dff_cons_total = df_cons_total.copy()
    fig3 = px.bar(data_frame=dff_cons_total, x='Annual Total', y='Total Energy Consumption')

    dff_cons_final_years = df_gen_total_final.copy()
    dff_cons_final_years = dff_cons_final_years[dff_cons_final_years['YEAR'] == value]
    dff_cons_final_years = dff_cons_final_years[dff_cons_final_years['ENERGY SOURCE'] != 'Total']
    fig4 = px.bar(data_frame=dff_cons_final_years, x='ENERGY SOURCE', y='GENERATION (Megawatthours)')

    dff_cons_total_years = df_cons_total.copy()
    dff_cons_total_years = dff_cons_total_years[dff_cons_total_years['Annual Total'] == value]
    fig5 = px.scatter(data_frame=dff_cons_total_years, x='Annual Total', y='Total Primary Energy Consumption')
    return fig, container, fig2, fig3, fig4, fig5
# ---------------------------------------

# Run the test server

# ---------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)