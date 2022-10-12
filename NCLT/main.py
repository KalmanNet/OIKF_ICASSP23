import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy.stats import chi2, norm
import os.path
from tabulate import tabulate
import scipy.stats as st

def main():
  
  data_GT_x, data_GT_y, data_GPS_x, data_GPS_y, time_GPS, time_GT = call_data()

  data_y = data_GPS_x
  data_GT = data_GT_x

  q_squared_vec = np.array((1e-3, 1e-4, 1e-7, 1e-6))
  r_squared_vec = np.array((1e2, 1e3, 1e4, 1e6)) 

  file_name_MSE_dB = 'P_MSE_dB.npy'
  file_name_MSE_m  = 'P_MSE_m.npy'
  file_name_x_hat  = 'x_hat.npy'
  
  if (os.path.isfile(file_name_x_hat) == True):
      x_hat = np.load(file_name_x_hat)

  else:
    x_hat = create_data_2_order(data_y, time_GPS, r_squared_vec, q_squared_vec)
    np.save('x_hat', x_hat)

  P_MSE_dB, P_MSE_m = MSE(time_GPS, data_GT, data_y, x_hat, q_squared_vec, r_squared_vec)
  np.save(file_name_MSE_dB, P_MSE_dB)
  np.save(file_name_MSE_m, P_MSE_m)

  min_vec = np.zeros(x_hat.shape[0] + 1)
  index_vec = np.zeros((x_hat.shape[0] + 1, 2))

  for i in range(x_hat.shape[0]):
    min_vec[i] = P_MSE_m[i, :, :].min()
    index = np.where(P_MSE_m[i, :] == min_vec[i])
    index_vec[i, :] = np.array(index)[:, 0]

  plot_MSE(data_y, x_hat, time_GPS, P_MSE_dB, P_MSE_m, index_vec)
 
if __name__ == "__main__":
    main()
