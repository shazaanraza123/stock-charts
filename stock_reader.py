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
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'Apple (AAPL)', 'value': 'AAPL'},
            {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
            {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
            {'label': 'Amazon (AMZN)', 'value': 'AMZN'}
        ],
        value='AAPL',  # Default value
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

    # Graph to display candlestick chart
    dcc.Graph(id='stock-chart')
])

# Callback to update the chart based on user input
@app.callback(
    Output('stock-chart', 'figure'),  # Output: Update the 'figure' property of 'stock-chart'
    [Input('stock-dropdown', 'value'),  # Input: Listen to changes in 'stock-dropdown'
     Input('interval-dropdown', 'value')]  # Input: Listen to changes in 'interval-dropdown'
)
def update_chart(ticker, interval):
    # Step 1: Fetch stock data
    stock = yf.Ticker(ticker)
    historical_data = stock.history(period="1mo", interval=interval)

    # Step 2: Handle empty data
    if historical_data.empty:
        return go.Figure().update_layout(
            title="No data available for the selected stock and interval",
            xaxis_title="Date",
            yaxis_title="Price (USD)"
        )

    # Step 3: Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=historical_data.index,
        open=historical_data['Open'],
        high=historical_data['High'],
        low=historical_data['Low'],
        close=historical_data['Close'],
        name="Candlestick"
    )])

    # Step 4: Add chart title and labels
    fig.update_layout(
        title=f"{ticker} Stock Price (Last 1 Month)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False
    )

    return fig  # Return the updated figure

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)