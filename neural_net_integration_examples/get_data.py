import tushare as ts


def get_stock_data(code, start_date, end_date, token):
    ts.set_token(token)
    pro = ts.pro_api()
    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
    df = df.sort_values(by="trade_date", ascending=True)  # 对data_folder进行排序，以便滑动窗口操作
    df.set_index("trade_date", inplace=True)
    return df


stock_code = "600036.SH"
start_date = "20200101"
end_date = "20220101"
api_token = "YOUR_API_TOKEN"

data = get_stock_data(stock_code, start_date, end_date, api_token)
data.to_csv('./data.csv')
print(data.head())
