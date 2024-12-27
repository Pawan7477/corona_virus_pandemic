import pandas as pd
import plotly.graph_objs as go
import dash
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load the data
patients = pd.read_csv('state_wise_daily data file IHHPET.csv')

# Clean up column names (remove leading/trailing spaces)
patients.columns = patients.columns.str.strip()

# Print column names and first few rows for debugging
print("Columns in the DataFrame:", patients.columns)
print(patients.head())

# Extract required total counts
total = patients.shape[0]  # Total rows in the dataset
active = patients[patients['Status'] == 'Confirmed'].shape[0]  # Confirmed cases count
recovered = patients[patients['Status'] == 'Recovered'].shape[0]  # Recovered cases count
deceased = patients[patients['Status'] == 'Deceased'].shape[0]  # Deceased cases count

# Define options for the dropdown
options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]

options1 = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Mask', 'value': 'Mask'},
    {'label': 'Sanitizer', 'value': 'Sanitizer'},
    {'label': 'Oxygen', 'value': 'Oxygen'}
]

options2 = [
    {'label': 'Red Zone', 'value': 'Red Zone'},
    {'label': 'Blue Zone', 'value': 'Blue Zone'},
    {'label': 'Green Zone', 'value': 'Green Zone'},
    {'label': 'Orange Zone', 'value': 'Orange Zone'}
]

# Initialize Dash app
app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css'])

# App layout
app.layout = html.Div([
    html.H1('Corona Virus Pandemic', style={'color': '#fff', 'text-align': 'center'}),

    # Cards for displaying the totals
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='text-light'),
                    html.H4(active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered Cases", className='text-light'),
                    html.H4(recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Deaths", className='text-light'),
                    html.H4(deceased, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3')
    ], className='row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='plot-graph', options=options1, value='All'),
                    dcc.Graph(id='graph')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-6'),

        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='my_dropdown', options=options2, value='Status',style={"width": "100%"}),
                    dcc.Graph(id='the_graph')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-6')
    ], className='row'),

    # Dropdown and graph
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value='All'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-12')
    ], className='row')
], className='container')


# Define the callback to update the bar chart
@app.callback(
    Output('bar', 'figure'),
    [Input('picker', 'value')]
)
def update_graph(type):
    print(f"Selected type: {type}")  # Debugging: print the selected value

    # Ensure the DataFrame and columns are as expected
    print("Columns available:", patients.columns)  # Debugging: print column names

    if type == 'All':
        return {
            'data': [go.Bar(x=patients['State'], y=patients['Confirmed'])],
            'layout': go.Layout(title='State Total Count', plot_bgcolor='orange')
        }
    elif type == 'Hospitalized':
        return {
            'data': [go.Bar(x=patients['State'], y=patients['Hospitalized'])],
            'layout': go.Layout(title='Hospitalized Cases by State', plot_bgcolor='orange')
        }
    elif type == 'Recovered':
        return {
            'data': [go.Bar(x=patients['State'], y=patients['Recovered'])],
            'layout': go.Layout(title='Recovered Cases by State', plot_bgcolor='orange')
        }
    elif type == 'Deceased':
        return {
            'data': [go.Bar(x=patients['State'], y=patients['Deceased'])],
            'layout': go.Layout(title='Deceased Cases by State', plot_bgcolor='orange')
        }
    return {
        'data': [],
        'layout': go.Layout(title='Invalid Category Selected', plot_bgcolor='white')
    }


@app.callback(Output('graph', 'figure'), [Input('plot-graph', 'value')])
def generate_graph(type):
    if type == 'All':
        return {
            'data': [go.Line(x=patients['Status'], y=patients['Confirmed'])],
            'layout': go.Layout(title='Commodities Total Count', plot_bgcolor='pink')
        }
    elif type == 'Mask':
        return {
            'data': [go.Line(x=patients['Status'], y=patients['Mask'])],
            'layout': go.Layout(title='Commodities Total Count', plot_bgcolor='pink')
        }
    elif type == 'Sanitizer':
        return {
            'data': [go.Line(x=patients['Status'], y=patients['Sanitizer'])],
            'layout': go.Layout(title='Commodities Total Count', plot_bgcolor='pink')
        }
    elif type == 'Oxygen':
        return {
            'data': [go.Line(x=patients['Status'], y=patients['Oxygen'])],
            'layout': go.Layout(title='Commodities Total Count', plot_bgcolor='pink')
        }


@app.callback(Output('the_graph', 'figure'), [Input('my_dropdown', 'value')])
def generate_pie_chart(my_dropdown):
    piechart = px.pie(data_frame=patients, names=my_dropdown, hole=0.3)
    return (piechart)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
