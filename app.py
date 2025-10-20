from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv('data/clean_used_cars_dataset.csv')

popular_brand_count = df['brand'].value_counts().reset_index()[:10]
popular_brand_count.columns = ['Brand', 'Count']
brands = popular_brand_count['Brand']
popular_brand = px.bar(popular_brand_count, x='Brand', y='Count', title="Top 10 Popular Brands")

popular_color_count = df['color'].value_counts().reset_index()[:10]
popular_color_count.columns = ['Color', 'Count']
colors = popular_color_count['Color']
popular_color = px.bar(popular_color_count, x='Color', y='Count', title="Top 10 Popular Car Colors")

mileage_hist = px.histogram(df, x='mileage_log', title="Distribution of Mileage")
price_hist = px.histogram(df, x='price_in_euro', title='Distribution of Price')

df_top_brands = df[df['brand'].isin(brands)]
brand_price_box = px.box(df_top_brands, x='brand', y='price_in_euro', title='Distribution of Price over Top Brands')
color_price_box = px.box(df, x='color', y='price_in_euro', title='Distribution of Price over Colors')

numeric_df = df[['year', 'price_log', 'power_log', 'mileage_log']]
corr = numeric_df.corr()
heatmap = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu",
    zmin=-1, zmax=1,
    title=  "Correlation Heatmap"
)


app = Dash()

app.layout = [
    html.H1(children='German Used Car Analysis', style={'textAlign':'center'}),
    html.Div(
        children=[
            html.H2(['Univarient Analysis'], style={'textAlign':'center'}),
            html.Div(children=[
                html.Div(children=[
                    html.P("Select Brand"),
                    dcc.Dropdown(
                        id='brand_dropdown',
                        options=brands,
                        value=brands,
                        multi=True
                    )
                ], style={'width':'50%', 'margin-left': '15px'}),
                html.Div(children=[
                    html.P("Select Color"),
                    dcc.Dropdown(
                        id='color_dropdown',
                        options=colors,
                        value=colors,
                        multi=True
                    )
                ], style={'width':'50%', 'margin': '0 15px 0 25px'}),
            ], style={'display': 'flex'}),
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(figure=popular_brand, id='popular_brand')
                ], style={'width':'50%'}),
                html.Div(children=[
                    dcc.Graph(figure=popular_color, id='popular_color')
                ], style={'width':'50%'}),
            ], style={'display': 'flex'}),
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(figure=mileage_hist, id='mileage_hist')
                ], style={'width':'50%'}),
                html.Div(children=[
                    dcc.Graph(figure=price_hist, id='price_hist')
                ], style={'width':'50%'}),
            ], style={'display': 'flex'}),
        ]
    ),
    html.Div(
        children=[
            html.H2(['Bivarient Analysis'], style={'textAlign':'center'}),
            html.Div(children=[
                html.Div(children=[
                    dcc.Graph(figure=brand_price_box, id='brand_price_box')
                ], style={'width':'50%'}),
                html.Div(children=[
                    dcc.Graph(figure=color_price_box, id='color_price_box')
                ], style={'width':'50%'}),
            ], style={'display': 'flex'}),
            html.Div(children=[
                dcc.Graph(figure=heatmap, id='heatmap')
            ]),
        ]
    ),
]

@callback(
    Output('popular_brand', 'figure'),
    Input('brand_dropdown', 'value')
)
def update_brand(value):
    dff = df[df['brand'].isin(value)]
    popular_brand_count = dff['brand'].value_counts().reset_index()[:10]
    popular_brand_count.columns = ['Brand', 'Count']
    return px.bar(popular_brand_count, x='Brand', y='Count', title="Top 10 Popular Brand")

@callback(
    Output('popular_color', 'figure'),
    Input('color_dropdown', 'value')
)
def update_color(value):
    dff = df[df['color'].isin(value)]
    popular_color_count = df['color'].value_counts().reset_index()[:10]
    popular_color_count.columns = ['Color', 'Count']
    return px.bar(popular_color_count, x='Color', y='Count', title="Top 10 Popular Colors")


if __name__ == '__main__':
    app.run(debug=True)
