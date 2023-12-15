from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from .model import SimpleLSTM
import backtrader as bt
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
import numpy as np

torch.manual_seed(888)
np.random.seed(888)

def create_dataset(stock_data, window_size):
    X = []
    y = []
    scaler = MinMaxScaler()
    stock_data_normalized = scaler.fit_transform(stock_data.values.reshape(-1, 1))

    for i in range(len(stock_data) - window_size - 2):
        X.append(stock_data_normalized[i:i + window_size])
        if stock_data.iloc[i + window_size + 2] > stock_data.iloc[i + window_size - 1]:
            y.append(1)
        else:
            y.append(0)

    X, y = np.array(X), np.array(y)
    X = torch.from_numpy(X).float()
    y = torch.from_numpy(y).long()
    return X, y, scaler

# 模型参数
input_size = 1
hidden_size = 64
num_layers = 2
num_classes = 2
window_size = 10

data = pd.read_csv('data.csv')
X, y, scaler = create_dataset(data['close'], window_size)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 创建 DataLoader
train_data = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

model = SimpleLSTM(input_size, hidden_size, num_layers, num_classes)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

num_epochs = 200

# 训练模型
for epoch in range(num_epochs):
    for i, (batch_X, batch_y) in enumerate(train_loader):
         # 前向传播
         outputs = model(batch_X)
         loss = criterion(outputs, batch_y)
         # 反向传播和优化
         optimizer.zero_grad()
         loss.backward()
         optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

print('Finished Training')
torch.save(model.state_dict(), 'rnn_model.pth')

model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    test_data = TensorDataset(X_test, y_test)
    test_loader = DataLoader(test_data, batch_size=32, shuffle=False)
    for batch_X, batch_y in test_loader:
          outputs = model(batch_X)
          _, predicted = torch.max(outputs.data, 1)
          total += batch_y.size(0)
          correct += (predicted == batch_y).sum().item()

print(f'Accuracy of the model on the test data: {100 * correct / total}%')

# 构建策略
class LSTMStrategy(bt.Strategy):

    def __init__(self):
        self.data_close = self.datas[0].close
        self.model = SimpleLSTM(input_size, hidden_size, num_layers, num_classes)
        self.model.load_state_dict(torch.load('rnn_model.pth'))
        self.model.eval()
        self.scaler = scaler
        self.counter = 1

    def next(self):
        if self.counter < window_size:
            self.counter += 1
            return
        previous_close_prices = [self.data_close[-i] for i in range(0, window_size)]
        X = torch.tensor(previous_close_prices).view(1, window_size, -1).float()
        X = self.scaler.transform(X.numpy().reshape(-1, 1)).reshape(1, window_size, -1)

        prediction = self.model(torch.tensor(X).float())
        max_vals, max_idxs = torch.max(prediction, dim=1)
        predicted_prob, predicted_trend = max_vals.item(), max_idxs.item()

        if predicted_trend == 1 and not self.position:  # 上涨趋势
            self.order = self.buy() # 买入股票
        elif predicted_trend == 0 and self.position:  # 如果预测不是上涨趋势且持有股票，卖出股票
            self.order = self.sell()


# Load test data
test_data = pd.read_csv('data.csv', index_col=0, parse_dates=True)

# Create a cerebro entity
cerebro = bt.Cerebro(runonce=False)

# Add data to cerebro
data = bt.feeds.PandasData(
    dataname=test_data,
    datetime=None,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=8,
    openinterest=-1)
cerebro.adddata(data)

# Add strategy to cerebro
cerebro.addstrategy(LSTMStrategy)

# 本金10000，每次交易100股
cerebro.broker.setcash(10000)
cerebro.addsizer(bt.sizers.FixedSize, stake=100)

# 万五佣金
cerebro.broker.setcommission(commission=0.0005)


# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
cerebro.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Plot the result
cerebro.plot()