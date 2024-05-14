import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import dash_ag_grid as dag


dash.register_page(__name__, path = "/categoryanalysis", title = "Category Analysis")

superstore = pd.read_csv("data/Sample - Superstore.csv", encoding = "latin1")

# Total Sold

categoryquantity = superstore.groupby('Category')['Quantity'].sum()

categoryquantitydistribution = px.pie(names=categoryquantity.index,
                                      values=categoryquantity.values,
                                      hole=0.7,
                                      color_discrete_sequence=px.colors.qualitative.Dark24_r)

categoryquantitydistribution.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)",
                                           legend_font_color='white', title=dict(font=dict(color='white')))

totalquantitysold = '{:,}'.format(categoryquantity.sum())
categoryquantitydistribution.add_annotation(text="Total Sold", showarrow=False,
                                            font_size=14, font_color='White',
                                            y=0.55)
categoryquantitydistribution.add_annotation(text=totalquantitysold, showarrow=False,
                                            font_size=14, font_color='White', y=0.45)


# Sub-Category Distribution

categorysubcategoryquantity = superstore.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()

categorysubcategorydistribution = px.sunburst(categorysubcategoryquantity, path=['Category', 'Sub-Category'],
                                               values='Quantity')

categorysubcategorydistribution.update_layout(paper_bgcolor='rgba(0,0,0,0)')

categorysubcategorydistribution.update_traces(marker=dict(colors=px.colors.qualitative.Dark24))


# City PercentageDistribution

cityquantitypercentage = superstore['Quantity'].sum()
cityquantitygrouped = superstore.groupby("City")['Quantity'].sum().nlargest(3)
cityquantitygroupedsum = cityquantitygrouped.sum()
percentagedistribution = (cityquantitygrouped / cityquantitypercentage) * 100
percentagelabels = [f"{city} : {percentage : .2f}%" for city, percentage in
                    zip(cityquantitygrouped.index, percentagedistribution)]

cityquantitypercentagedistribution = px.pie(names=percentagelabels,
                                            values=cityquantitygrouped.values,
                                            hole=0.7,
                                            color_discrete_sequence=px.colors.qualitative.Dark24_r)

cityquantitypercentagedistribution.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)",
                                                 legend_font_color='white',
                                                 title=dict(font=dict(color='white')))

cityquantitypercentagedistribution.add_annotation(text="Top 3 Cities", showarrow=False,
                                                  font_size=14, font_color='White',
                                                  y=0.6)

cityquantitypercentagedistribution.add_annotation(text="Total Sold", showarrow=False,
                                                  font_size=14, font_color='White',
                                                  y=0.5)

cityquantitypercentagedistribution.add_annotation(text='{:,}'.format(cityquantitygroupedsum), showarrow=False,
                                                  font_size=14, font_color='White', y=0.4)

# Country Distribution

countryquantity = superstore.groupby('Country')['Quantity'].sum().reset_index()

countryquantitydistribution = px.scatter_geo(countryquantity, locations = countryquantity['Country'],
                                            locationmode = "country names",
                                            size = countryquantity.groupby("Country")['Quantity'].sum().values,
                                            color = countryquantity.groupby("Country")['Quantity'].sum().values,
                                            projection = "natural earth", color_continuous_scale = "magma_r")

countryquantitydistribution.update_layout(paper_bgcolor = "rgba(0,0,0,0)",
                                          geo = dict(
                                            bgcolor = "rgba(0,0,0,0)",
                                            landcolor = 'slategrey', showcountries = True,
                                            showcoastlines = True
                                          ))

countryquantitydistribution.update_geos(showframe = True)

countryquantitydistribution.update_coloraxes(colorbar_title = "Quantity Sold", colorbar_title_font_color = 'White', colorbar_tickfont = dict(color = 'white'))


# City Distribution 

cityquantity = superstore.groupby(['City', 'Sub-Category'])['Quantity'].sum().reset_index()
cityquantitytop5 = cityquantity.groupby('City')['Quantity'].sum().nlargest(3).index
cityquantitytop5final = cityquantity[cityquantity['City'].isin(cityquantitytop5)]

cityquantitydistribution = px.bar(cityquantitytop5final, x = "City", y = "Quantity",
                                  color = 'Sub-Category', barmode = 'group',
                                  text = 'Quantity', color_discrete_sequence = px.colors.qualitative.Dark24_r)

cityquantitydistribution.update_layout(yaxis = dict(showticklabels = False), 
                                       xaxis = dict(tickfont = dict(color = 'white'), categoryorder = "total descending"),
                                       yaxis_title = "", xaxis_title = "",
                                       paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
                                       legend_title_font_color = 'White', legend_font_color = 'White', bargap = 0.1)

cityquantitydistribution.update_yaxes(showgrid = False, gridcolor = 'rgba(0,0,0,0)', zeroline = False, zerolinecolor = "rgba(0, 0, 0, 0)")

cityquantitydistribution.update_traces(marker_line_width = 0, textposition = "outside", textfont_color = 'white', textfont_size = 14, cliponaxis = False)


# Product Trend

superstore['Order Date'] = pd.to_datetime(superstore['Order Date'], format = "%m/%d/%Y")

monthlycategorytrend = superstore.groupby(['Category', pd.Grouper(key = "Order Date", freq = 'ME')])['Quantity'].sum().reset_index()

monthlycategorytrenddistribution = px.line(monthlycategorytrend, x = "Order Date", y = "Quantity", color = 'Category',
                                           title = 'Monthly Trend of Goods Sold', line_shape = "spline")

monthlycategorytrenddistribution.update_layout(yaxis = dict(showticklabels = False), 
                                       xaxis = dict(tickfont = dict(color = 'white'), categoryorder = "total descending"),
                                       yaxis_title = "", xaxis_title = "",
                                       paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
                                       title = dict(font = dict(color = 'white')),
                                       legend_title_font_color = 'White', legend_font_color = 'White')

monthlycategorytrenddistribution.update_yaxes(showgrid = False, gridcolor = 'rgba(0,0,0,0)', zeroline = False, zerolinecolor = "rgba(0, 0, 0, 0)")
monthlycategorytrenddistribution.update_xaxes(showgrid = False, gridcolor = 'rgba(0,0,0,0)', zeroline = False, zerolinecolor = "rgba(0, 0, 0, 0)")

#Dash Table

products_table= dash_table.DataTable(
   superstore.to_dict('records'), 
   columns= [{"id": "Product ID", "name": "Product ID"}, {"id": "Product Name", "name": "Product Name"}, {"id": "Profit", "name":"Profit"}],
   fixed_rows={'headers': True},
   style_table= {'height':'300px', 'overflowY': 'auto'},
   style_cell={'padding': '5px'},
   style_header={
        'backgroundColor': 'black',
        'fontWeight': 'bold',
        'color': 'white'
    },
   style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(240, 220, 220)',
        },
        {
            'if': {
                'filter_query': '{Profit} < "0"',
                'column_id': 'Profit'
            },
            'backgroundColor': 'red',
            'color': 'white'
        }

    ],
   style_cell_conditional=[
        {'if': {'column_id': 'Product ID'},
         'width': '20%'},
        {'if': {'column_id': 'Product Name'},
         'width': '60%'},
        {'if': {'column_id': 'Profit'},
         'width': '20%'},
    ]
)

layout = html.Div(
    children = [
        dbc.Col(
                 dcc.Dropdown(
                    superstore['Segment'].unique(),
                    placeholder= "Select a segment",
                    style={"background": "black"},
                    value="Consumer",
                    id = "segment_dropdown"
                    )
                ),    
        dbc.Row(
            children = [
                dbc.Col(
                    children = dcc.Graph(id='category_quantity_distribution')
                ),
                dbc.Col(
                    children = dcc.Graph(id = 'category_subcategory_distribution')
                ),
                dbc.Col(
                    children = dcc.Graph(id='city_quantity_percentage_distribution', responsive = True)
                ),
            ]
        ),
      dbc.Row(
         children = [
            dbc.Col(
               dcc.Graph(figure=countryquantitydistribution, responsive = True)
            ),
            dbc.Col(
               dcc.Graph(id='city_quantity_distribution', responsive = True)
            ),
         ]
      ),
      dbc.Row(
         children = [
            dbc.Col(
               dcc.Graph(figure=monthlycategorytrenddistribution, responsive = False)
            )
         ]
      ),
      dbc.Row(
         children = [
            products_table
         ]
      )
    ]
)

@callback(
    Output("category_quantity_distribution", "figure"),
    Output("category_subcategory_distribution", "figure"),
    Output("city_quantity_percentage_distribution", "figure"),
    Input("segment_dropdown",'value')
)
def multiple_outputs_single_input(segment_value):
    if(segment_value):
      segment_filter_superstore=superstore[superstore['Segment']== segment_value]
      categoryquantity = segment_filter_superstore.groupby('Category')['Quantity'].sum()
      categorysubcategoryquantity = segment_filter_superstore.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()
      cityquantitygrouped = segment_filter_superstore.groupby("City")['Quantity'].sum().nlargest(3)

    else:
      categoryquantity = superstore.groupby('Category')['Quantity'].sum()
      categorysubcategoryquantity = superstore.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()
      cityquantitygrouped = superstore.groupby("City")['Quantity'].sum().nlargest(3)

#totalsold
    categoryquantity = superstore.groupby('Category')['Quantity'].sum()

    categoryquantitydistribution = px.pie(names=categoryquantity.index,
                                      values=categoryquantity.values,
                                      hole=0.7,
                                      color_discrete_sequence=px.colors.qualitative.Dark24_r)

    categoryquantitydistribution.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)",
                                           legend_font_color='white', title=dict(font=dict(color='white')))

    totalquantitysold = '{:,}'.format(categoryquantity.sum())
    categoryquantitydistribution.add_annotation(text="Total Sold", showarrow=False,
                                            font_size=14, font_color='White',
                                            y=0.55)
    categoryquantitydistribution.add_annotation(text=totalquantitysold, showarrow=False,
                                            font_size=14, font_color='White', y=0.45)     


# Sub-Category Distribution

    categorysubcategoryquantity = superstore.groupby(['Category', 'Sub-Category'])['Quantity'].sum().reset_index()

    categorysubcategorydistribution = px.sunburst(categorysubcategoryquantity, path=['Category', 'Sub-Category'],
                                               values='Quantity')

    categorysubcategorydistribution.update_layout(paper_bgcolor='rgba(0,0,0,0)')

    categorysubcategorydistribution.update_traces(marker=dict(colors=px.colors.qualitative.Dark24))    
 
# City PercentageDistribution

    cityquantitypercentage = superstore['Quantity'].sum()
    cityquantitygrouped = superstore.groupby("City")['Quantity'].sum().nlargest(3)
    cityquantitygroupedsum = cityquantitygrouped.sum()
    percentagedistribution = (cityquantitygrouped / cityquantitypercentage) * 100
    percentagelabels = [f"{city} : {percentage : .2f}%" for city, percentage in
                    zip(cityquantitygrouped.index, percentagedistribution)]

    cityquantitypercentagedistribution = px.pie(names=percentagelabels,
                                            values=cityquantitygrouped.values,
                                            hole=0.7,
                                            color_discrete_sequence=px.colors.qualitative.Dark24_r)

    cityquantitypercentagedistribution.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)",
                                                 legend_font_color='white',
                                                 title=dict(font=dict(color='white')))

    cityquantitypercentagedistribution.add_annotation(text="Top 3 Cities", showarrow=False,
                                                  font_size=14, font_color='White',
                                                  y=0.6)

    cityquantitypercentagedistribution.add_annotation(text="Total Sold", showarrow=False,
                                                  font_size=14, font_color='White',
                                                  y=0.5)

    cityquantitypercentagedistribution.add_annotation(text='{:,}'.format(cityquantitygroupedsum), showarrow=False,
                                                  font_size=14, font_color='White', y=0.4)   

    return categoryquantitydistribution,categorysubcategorydistribution,cityquantitypercentagedistribution

@callback(
   Output("city_quantity_distribution", 'figure'),
   Input("category_quantity_distribution", 'clickData')
)
def interactive_cross_filtering(clicked_category_value):
   if (clicked_category_value):
      segment_filter_superstore=superstore[superstore['Category']== clicked_category_value['points'][0]['label']]
      cityquantity = segment_filter_superstore.groupby(['City', 'Sub-Category'])['Quantity'].sum().reset_index()
   else:
      segment_filter_superstore=superstore[superstore['Category']== clicked_category_value]
      cityquantity = superstore.groupby(['City', 'Sub-Category'])['Quantity'].sum().reset_index()
   
   cityquantitytop5 = cityquantity.groupby('City')['Quantity'].sum().nlargest(3).index
   cityquantitytop5final = cityquantity[cityquantity['City'].isin(cityquantitytop5)]

   cityquantitydistribution = px.bar(cityquantitytop5final, x = "City", y = "Quantity",
                                    color = 'Sub-Category', barmode = 'group',
                                    text = 'Quantity', color_discrete_sequence = px.colors.qualitative.Dark24_r)

   cityquantitydistribution.update_layout(yaxis = dict(showticklabels = False), 
                                          xaxis = dict(tickfont = dict(color = 'white'), categoryorder = "total descending"),
                                          yaxis_title = "", xaxis_title = "",
                                          paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
                                          legend_title_font_color = 'White', legend_font_color = 'White', bargap = 0.1)

   cityquantitydistribution.update_yaxes(showgrid = False, gridcolor = 'rgba(0,0,0,0)', zeroline = False, zerolinecolor = "rgba(0, 0, 0, 0)")

   cityquantitydistribution.update_traces(marker_line_width = 0, textposition = "outside", textfont_color = 'white', textfont_size = 14, cliponaxis = False)

   return cityquantitydistribution
