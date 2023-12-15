import os
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py 
import dash
from dash import dcc                  # 交互式组件
from dash import html                 # 代码转html
from dash.dependencies import Input, Output         # 回调
import dash_bootstrap_components as dbc 

### 数据预处理，读取相关的数据
datas = {}
result = []
file_list = os.listdir("./玻璃-DualThrust参数优化结果/参数优化结果/")
for file in file_list:
    print(file)
    df = pd.read_csv("./玻璃-DualThrust参数优化结果/参数优化结果/"+file,index_col=0)
    df['datetime']=pd.to_datetime(df.index)
    param = file[:-4] 
    look_back_days,k1,k2,sharpe_ratio,annual_return,max_drawdown,trade_num = param.split("__")
    datas[look_back_days+"_"+k1+"_"+k2] = df
    result.append([look_back_days,k1,k2,sharpe_ratio,annual_return,max_drawdown,trade_num])
data = pd.DataFrame(result,columns=['look_back_days','k1','k2','sharpe_ratio','annual_return','max_drawdown','trade_num'])
data = data.astype("float")
### 运行dash
app = dash.Dash('玻璃-DualThrust参数优化结果')

app.layout =  html.Div([

    html.Div([
            dcc.Dropdown(
                id = 'indicator_value',
                options = [{'label': i, 'value': i} for i in sorted([float(i) for i in data['look_back_days'].unique()])],
                value = 50),
            dcc.Graph(id = 'crossfilter-indicator-heatmap',
            hoverData = dict(points = [{'customdata': ('60','1.0','1.0')}]))
                ],
            style = dict(width = '49%', display = 'inline-block')),

    # 设置交互数据对象及默认值
    html.Div([
        # 设置交互的子图表
        dcc.Graph(id = 'value-time-series')],
        style = dict(width = '49%', display = 'inline-block')),  
])


# 回调1个指标值
@app.callback(
    Output('crossfilter-indicator-heatmap', 'figure'),
    [ Input('indicator_value', 'value'),
     ])
def update_figure(indicator_value):
    df = data[data['look_back_days']==float(indicator_value)]
    print(df.tail())
    df['text']="look_back_days"+" : "+df['look_back_days'].astype("str")+"<br>"+\
            "k1"+" : "+df['k1'].astype("str")+"<br>"+\
            "k2"+" : "+df['k2'].astype("str")+"<br>"+\
            "sharpe_ratio"+" : "+df['sharpe_ratio'].astype("str")+"<br>"+\
            "annual_return"+" : "+df['annual_return'].astype("str")+"<br>"+\
            "max_drawdown"+" : "+df['max_drawdown'].astype("str")+"<br>"+\
            "trade_num"+" : "+df['trade_num'].astype("str")+"<br>"
    # print(df.head())
    layout = go.Layout(
            # plot_bgcolor='red',  # 图背景颜色
            paper_bgcolor='white',  # 图像背景颜色
            autosize=True,
            width=600,
            height=600,
            title='策略-热力图',
            titlefont=dict(size=30, color='gray'),

            # 图例相对于左下角的位置
            legend=dict(
                x=0.02,
                y=0.02
            ),

            # x轴的刻度和标签
            xaxis=dict(title='k1',  # 设置坐标轴的标签
                    titlefont=dict(color='red', size=20),
                    tickfont=dict(color='blue', size=18, ),
                    tickangle=45,  # 刻度旋转的角度
                    showticklabels=True,  # 是否显示坐标轴
                    ),

            # y轴的刻度和标签
            yaxis=dict(title='k2',  # 坐标轴的标签
                    titlefont=dict(color='blue', size=18),  # 坐标轴标签的字体及颜色
                    tickfont=dict(color='green', size=20, ),  # 刻度的字体大小及颜色
                    showticklabels=True,  # 设置是否显示刻度
                    tickangle=-45,
                    # 设置刻度的范围及刻度
                    autorange=True,
                    # range=[0, 100],
                    # type='linear',
                    ),
        )
    fig = go.Figure(data=go.Heatmap(
            showlegend=True,
            name='数据',
            x=df["k1"],
            y=df['k2'],
            z=df['sharpe_ratio'],
            type='heatmap',
            text = df['text'],
            customdata = df[["look_back_days","k1",'k2']],
            hoverinfo = "text",
            hovertext = df['text']),
        layout=layout
    )
 
    fig.update_layout(margin=dict(t=100, r=150, b=100, l=100), autosize=True),
    
    return fig 
    

# # 回调--设置上子图表的交互
@app.callback(
    Output('value-time-series', 'figure'),
    [Input('crossfilter-indicator-heatmap', 'hoverData'),
     ])
def update_figure(hoverData):
    look_back_days,k1,k2 = hoverData['points'][0]['customdata']
    key = str(look_back_days)+"_"+str(k1)+"_"+str(k2)
    # print(datas.keys())
    data = datas[key]
    data.index = pd.to_datetime(data.index)
    layout = go.Layout(
            # plot_bgcolor='red',  # 图背景颜色
            paper_bgcolor='white',  # 图像背景颜色
            autosize=True,
            width=800,
            height=600,)
    fig = go.Figure(data=go.Scatter(
            showlegend=True,
            name=f"{look_back_days}__{k1}__{k2}的资产曲线",
            x=data.index,
            y=data['value'],
            
        ),layout = layout)
    
    return fig 

app.run_server()