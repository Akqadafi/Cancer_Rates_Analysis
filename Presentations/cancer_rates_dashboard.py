import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the data
df = pd.read_csv(r"Q:\Downloads\Data Projects\Datasets\Cancer Research\Final Data Sets\Merged_Cancer_Rates_with_Survival_Rate.csv")

# Important features and targets
important_features = ['Bachelors Degree', 'Hispanic Pct.', 'Poverty Below 150%', 'SES', 'Unemployment Rate', 'White Pct', 'Black Pct.', 'Asian/PI Pct', 'AI/AN Pct']
targets = ['Death Rate', 'Incidence Rate', 'Survival Rate']

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Cancer Rates Dashboard"),
    
    html.Div([
        html.Div([
            html.Label("Select States:"),
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': state, 'value': state} for state in sorted(df['States'].unique())],
                value=[],
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Select Urbanicity:"),
            dcc.Dropdown(
                id='urbanicity-dropdown',
                options=[{'label': urb, 'value': urb} for urb in sorted(df['Urbanicity'].unique())],
                value=[],
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Select X-axis:"),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options=[{'label': feature, 'value': feature} for feature in important_features],
                value='Bachelors Degree'
            )
        ], style={'width': '20%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Select Y-axis:"),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=[{'label': target, 'value': target} for target in targets],
                value='Death Rate'
            )
        ], style={'width': '20%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
    html.Div([
        dcc.Graph(id='scatter-plot', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='correlation-heatmap', style={'width': '48%', 'display': 'inline-block'})
    ]),
    
    dcc.Graph(id='parallel-coordinates-plot')
])

# Callback for updating scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('urbanicity-dropdown', 'value'),
     Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_scatter_plot(selected_states, selected_urbanicity, x_axis, y_axis):
    filtered_df = df
    if selected_states:
        filtered_df = filtered_df[filtered_df['States'].isin(selected_states)]
    if selected_urbanicity:
        filtered_df = filtered_df[filtered_df['Urbanicity'].isin(selected_urbanicity)]
    
    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, hover_data=['County', 'States'],
                     color='Urbanicity', title=f'{x_axis} vs {y_axis}')
    return fig

# Callback for updating correlation heatmap
@app.callback(
    Output('correlation-heatmap', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('urbanicity-dropdown', 'value')]
)
def update_correlation_heatmap(selected_states, selected_urbanicity):
    filtered_df = df
    if selected_states:
        filtered_df = filtered_df[filtered_df['States'].isin(selected_states)]
    if selected_urbanicity:
        filtered_df = filtered_df[filtered_df['Urbanicity'].isin(selected_urbanicity)]
    
    corr_matrix = filtered_df[important_features + targets].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        zmin=-1,
        zmax=1
    ))
    fig.update_layout(title='Correlation Heatmap', height=600)
    return fig

# Callback for updating parallel coordinates plot
@app.callback(
    Output('parallel-coordinates-plot', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('urbanicity-dropdown', 'value')]
)
def update_parallel_coordinates_plot(selected_states, selected_urbanicity):
    filtered_df = df
    if selected_states:
        filtered_df = filtered_df[filtered_df['States'].isin(selected_states)]
    if selected_urbanicity:
        filtered_df = filtered_df[filtered_df['Urbanicity'].isin(selected_urbanicity)]
    
    fig = px.parallel_coordinates(filtered_df, 
                                  dimensions=important_features + targets,
                                  color='Death Rate',
                                  color_continuous_scale=px.colors.diverging.RdYlBu,
                                  title='Parallel Coordinates Plot of Important Features and Cancer Rates')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)

print("The updated Dash app code has been created and is ready to run.")
print("To start the dashboard, run this script with Python: python cancer_rates_dashboard.py")
print("Then open a web browser and go to http://127.0.0.1:8080/ to view the dashboard.")
