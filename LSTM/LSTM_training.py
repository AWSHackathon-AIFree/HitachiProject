import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Input
from keras.models import Model, load_model

data_thai = pd.read_excel('Simulation_data.xlsx', sheet_name = 'zone1')

data_thai = data_thai.dropna()

linear_trans_temp = []
for i in data_thai['Zone1 Air Temperature (C) adjust']:
  if i < 25:
    linear_trans_temp.append(i * 0.8)
  else:
    linear_trans_temp.append(i * 1.15)
data_thai['linear_trans_temp'] = linear_trans_temp
data_thai['linear_trans_temp'].min()
inside_temp = data_thai['linear_trans_temp'].values
set_temp = data_thai['Zone1 Cooling Setpoint Temperature(C)'].values

ac = []
for i in set_temp:
  if i == 24:
    ac.append(1)
  else:
    ac.append(0)
data_thai['ac'] = ac


# 創建數據集函數
def create_dataset(series, time_steps):
    X, y = [], []
    for i in range(len(series) - time_steps):
        X.append(series[i:i+time_steps])
        y.append(series[i+time_steps])
    return np.array(X), np.array(y)

time_steps = 3  # 使用過去3小時的數據進行預測
inside_temp_x, inside_temp_y = create_dataset(inside_temp, time_steps)
acc_x, acc_y = create_dataset(ac, time_steps)
inside_temp_x = inside_temp_x.reshape((inside_temp_x.shape[0], inside_temp_x.shape[1], 1))
acc_x = acc_x.reshape((acc_x.shape[0], acc_x.shape[1], 1))
concat_data =  np.concatenate((inside_temp_x, acc_x), axis = 2)
# 分割訓練集和測試集

def model_training(X, y, col_name):
  train_size = int(len(X) * 0.8)
  test_size = len(X) - train_size
  x_train, x_test = X[0:train_size], X[train_size:len(X)]
  y_train, y_test = y[0:train_size], y[train_size:len(y)]
  acc_train, acc_test = acc_x[0:train_size], acc_x[train_size:len(acc_x)]

  # 構建模型
  model = Sequential()
  model.add(LSTM(40, input_shape = (time_steps, x_train.shape[2])))
  model.add(Dense(1))

  # 編譯模型
  model.compile(loss='mean_squared_error', optimizer='adam')

  # 訓練模型
  history  = model.fit(x_train, y_train, epochs = 10, batch_size = 1, verbose = 2)

  # 預測
  # test_predict = model.predict([x_test, acc_test[3:]])
  test_predict = model.predict(x_test)
  # 評估模型
  test_score = model.evaluate(x_test, y_test, verbose=0)
  print(f'Test Score: {test_score:.2f} MSE')
  plt.plot(history.history['loss'], label = 'train')
  plt.legend()
  plt.show()
  plt.plot(model.predict(x_test)[:20], label='Predicted')
  plt.plot(y_test[:20], label='Actual')
  plt.title(f'{col_name}')
  plt.legend()
  plt.show()
  return model, x_train, x_test, y_train, y_test
inside_model, inside_x_train, inside_x_test, inside_y_train, inside_y_test = model_training(concat_data, inside_temp_y, 'inside_temp')

inside_model.save('indoor_temp_model.h5')