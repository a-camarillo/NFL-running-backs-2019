import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output

import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/a-camarillo/NFL-running-backs-2019/master/Data%20Cleaning/rushing_stats_2019')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='graph-with-slider',
            clickData={'points':[{'text': 'Dalvin Cook'}]}),
        dcc.Slider(
         id='week-slider',
         min=df['week'].min(),
         max=df['week'].max(),
         value=df['week'].min(),
         marks={str(week): 'Week {}'.format(week) for week in df['week'].unique()},
            step=None
        )
    ]),
    html.Div([
        dcc.Graph(id='line-graph')
    ])
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('week-slider', 'value')])
def update_figure(selected_week):
    filtered_df = df[df.week == selected_week]
    traces = []
    for i in filtered_df.player.unique():
        df_by_player = filtered_df[filtered_df['player'] == i]
        traces.append(dict(
            x=df_by_player['tot_yds'],
            y=df_by_player['tot_att'],
            text=df_by_player['player'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line' : {'width': 0.5, 'color': 'white'}
            },
            name=i  
        ))
    return {
        'data': traces,
        'layout':dict(
            xaxis={'type':'scatter','title':'Yards'},
            yaxis={'type':'scatter','title':'Attempts'},
            hovermode='closest',
            transition = {'duration': 500}
        )
    }

@app.callback(
    Output('line-graph', 'figure'),
    [Input('graph-with-slider', 'clickData')])
def update_linegraph(clickData):
    player_name = clickData['points'][0]['text']
    player_df = df[df.player == player_name]
    return {
        'data':[dict(
            x=player_df['week'],
            y=player_df['yds']
        )],
        'layout': dict(
            xaxis={'title':'Week'},
            yaxis={'title':'Yards'},
            title=player_name 
    )
}



if __name__ == '__main__':
    app.run_server(debug=True)