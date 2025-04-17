import yfinance as yf
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Interactive Stock Price Chart", style={'textAlign': 'center'}),

    # Dropdown for selecting stock ticker
    html.Label("Select stock: "),
    dcc.Input(
        id='stock-input',
        type='text',
        placeholder='Enter a stock ticker',
        value='AAPL',  # placeholder
        style={'width': '50%'},
    ),

    # Dropdown for selecting data period
    html.Label("Select data period: "),
    dcc.Dropdown(
        id='period-dropdown',
        options=[
            {'label': '1 Day', 'value': '1d'},
            {'label': '5 Days', 'value': '5d'},
            {'label': '1 Month', 'value': '1mo'},
            {'label': '3 Months', 'value': '3mo'},
            {'label': '6 Months', 'value': '6mo'},
            {'label': '1 Year', 'value': '1y'},
            {'label': '5 Years', 'value': '5y'},
            {'label': 'Max', 'value': 'max'},
        ],
        value='1mo',
        style={'width': '50%'}
    ),

    # Dropdown for selecting time interval
    html.Label("Select time interval: "),
    dcc.Dropdown(
        id='interval-dropdown',
        options=[
            {'label': '1 Hour', 'value': '1h'},
            {'label': '1 Day', 'value': '1d'},
            {'label': '1 Week', 'value': '1wk'}
        ],
        value='1h',  # Default value
        style={'width': '50%'}
    ),

    # Dropdown for selecting chart type
    html.Label("Select chart type: "),
    dcc.Dropdown(
        id='chart-type-dropdown',
        options=[
            {'label': 'Candlestick', 'value': 'candlestick'},
            {'label': 'Line', 'value': 'line'}
        ],
        value='candlestick',  # Default value
        style={'width': '50%'}
    ),

    # Graph to display candlestick chart
    dcc.Graph(id='stock-chart')
])

# Callback to update the chart based on user input
@app.callback(
    Output('stock-chart', 'figure'),  # Output: Update the 'figure' property of 'stock-chart'
    [Input('stock-input', 'value'),  # Input: Listen to changes in 'stock-dropdown'
     Input('interval-dropdown', 'value'),
     Input('chart-type-dropdown', 'value'),
     Input('period-dropdown', 'value')]  # Input: Listen to changes in 'period-dropdown'
)
def update_chart(ticker, interval, chart_type, period):
    # Step 1: Fetch stock data
    stock = yf.Ticker(ticker)
    historical_data = stock.history(period=period, interval=interval)

    # Step 2: Handle empty data
    if historical_data.empty:
        return go.Figure().update_layout(
            title="No data available for the selected stock and interval",
            xaxis_title="Date",
            yaxis_title="Price (USD)"
        )
    
    # Step 3: Create a candlestick chart
    if chart_type == 'candlestick':
        fig = go.Figure(data=[go.Candlestick(
            x=historical_data.index,
            open=historical_data['Open'],
            high=historical_data['High'],
            low=historical_data['Low'],
            close=historical_data['Close'],
            name="Candlestick"
        )])
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), dict(pattern="hour", bounds=[16, 9.5])])
        fig.update_layout(xaxis_rangeslider_visible=False)

    elif chart_type == 'line':
        fig = go.Figure(data=[go.Scatter(
            x=historical_data.index,
            y=historical_data['Close'],
            mode='lines',
            name='Line Chart'
        )]) 
        
    else:
        # Handle invalid chart_type
        fig = go.Figure()
        fig.add_annotation(
            text="Invalid chart type selected",
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig  # Return the updated figure

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)