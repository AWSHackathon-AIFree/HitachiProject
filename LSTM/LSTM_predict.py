import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
import pandas as pd

data = pd.read_excel(r'Simulation_data.xlsx', sheet_name = 'zone1')
class Predict():
    def __init__(self, model_path, future_steps, data):
        self.model = load_model(model_path)
        self.future_steps = future_steps
        self.data = data

    def create_dataset(self, series):
        X, y = [], []
        for i in range(len(series) - 3):
            X.append(series[i:i + 3])
            y.append(series[i + 3])
        return np.array(X), np.array(y)

    def generate_data(self):
      set_temp = self.data['Zone1 Cooling Setpoint Temperature(C)'].values
      ac = [1 if temp == 24 else 0 for temp in set_temp]
      self.data['ac'] = ac

    def predict_with_ac_off(self, current_data):
        predictions = []
        predictions.append(current_data[0, -1, 0])
        for i in range(2):
            pred = self.model.predict(current_data)[0, 0]
            predictions.append(pred)
            new_input_temp = np.append(current_data[0, 1:, 0], pred).reshape(1, 3, 1)
            ac_state = [1, 1, 0] if i == 0 else [1, 0, 0]
            current_data = np.concatenate((new_input_temp, np.array(ac_state).reshape(1, 3, 1)), axis=2)
        for _ in range(self.future_steps - 2):
            pred = self.model.predict(current_data)[0, 0]
            predictions.append(pred)
            new_input_temp = np.append(current_data[0, 1:, 0], pred).reshape(1, 3, 1)
            current_data = np.concatenate((new_input_temp, np.zeros((1, 3, 1))), axis=2)
        return predictions

    def predict_with_ac_on(self, current_data):
        predictions = []
        predictions.append(current_data[0, -1, 0])
        for _ in range(self.future_steps):
            pred = self.model.predict(current_data)[0, 0]
            predictions.append(pred)
            new_input_temp = np.append(current_data[0, 1:, 0], pred).reshape(1, 3, 1)
            current_data = np.concatenate((new_input_temp, np.ones((1, 3, 1))), axis=2)
        return predictions, current_data

    def last_known_data_create(self):
        inside_x_test, _ = self.create_dataset(self.data['Zone1 Air Temperature (C)'].values)
        acc_x, _ = self.create_dataset(self.data['ac'].values)

        inside_x_test = inside_x_test.reshape((inside_x_test.shape[0], inside_x_test.shape[1], 1))
        acc_x = acc_x.reshape((acc_x.shape[0], acc_x.shape[1], 1))
        combined_x = np.concatenate((inside_x_test, acc_x), axis=2)
        last_known_data = combined_x[-1].reshape(1, 3, 2)
        return last_known_data

    def plot_results_temp(self, last_known):
        predictions_ac_off = self.predict_with_ac_off(last_known)
        predictions_ac_on, current = self.predict_with_ac_on(last_known)
        plt.plot(range(1, 4), last_known[0, :, 0],  label='Actual Last 3 Steps')
        plt.plot(range(3, self.future_steps + 4), predictions_ac_off, label='AC Off')
        plt.plot(range(3, self.future_steps + 4), predictions_ac_on, label='AC On')
        plt.axvline(x=3, color='gray', linestyle='dashed', linewidth=1)
        plt.title('Predicted Inside Temperature')
        plt.xlabel('Future Time Steps')
        plt.ylabel('Temperature')
        plt.legend()
        plt.show()

    def ac_control(self, on_or_off):
      last_known = self.last_known_data_create()
      pred = self.model(last_known).numpy()[0][0]
      pred_ac = [pred, on_or_off]
      new_pred = np.append(last_known[:,1:], pred_ac).reshape(1, 3, 2)
      predictions_ac_off = self.predict_with_ac_off(new_pred)
      predictions_ac_on, current = self.predict_with_ac_on(new_pred)
      plt.plot(range(1, 4), new_pred[0, :, 0] ,label='Actual Last 3 Steps')
      plt.plot(range(3, self.future_steps + 4), predictions_ac_off, label='AC Off')
      plt.plot(range(3, self.future_steps + 4), predictions_ac_on, label='AC On')
      plt.axvline(x=3, color='gray', linestyle='dashed', linewidth=1)
      plt.title('Predicted Inside Temperature')
      plt.xlabel('Future Time Steps')
      plt.ylabel('Temperature')
      plt.legend()
      plt.show()


def launch():
  model_path = r'indoor_temp_model.h5'
  current_data = np.array([[31, 0], [30, 0], [30, 0]]).reshape(1, 3, 2)
  temp = Predict(model_path, 10, data)
  temp.generate_data()
  temp.plot_results_temp(current_data)

launch()