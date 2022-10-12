import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy.stats import chi2, norm
import os.path
from tabulate import tabulate
import time
from datetime import timedelta
from sklearn.metrics import confusion_matrix
from scipy.stats import bernoulli,rayleigh

def main():
   
  r_squared_vec = np.array((10, 1, 0.1, 0.01, 0.001))
  r_squared_vec_dB = -10 * np.log10(r_squared_vec)
  
  p = 0.2
  scl = 30

  del_t = 1e-1
  end_time = 10
  time_t = np.linspace(0, end_time,  int((end_time/del_t))+1)

  data_GT = np.load('data_GT.npy')
  data_y = np.load('data_y_p='+str(p)+'_scl='+str(scl)+'.npy')
  print(data_GT.shape)
  N = data_GT.shape[3]
  
  if os.path.isfile('data_y_new_p='+str(p)+"_scl="+str(scl)+'.npy')==True:
    data_y_new   = np.load('data_y_new_p='+str(p)+"_scl="+str(scl)+'.npy')
  else:
  
    data_y_new = data_y
    data_y_new[1,1,:,:,:]=data_y_new[1,0,:,:,:]
    for j in range(data_y.shape[4]):
      for i in range(len(r_squared_vec)):
          outliers = bernoulli.rvs(p, size=len(time_t))
          index = np.where(outliers == 1)[0]
          ray = rayleigh.rvs(size=len(index),scale=scl)
          data_y_new[1,1,index,i,j] = data_y[1,0,index,i,j] + ray

    np.save('data_y_new_p='+str(p)+"_scl="+str(scl)+'.npy', data_y_new)
    
  if (os.path.isfile('x_hat_noisy.npy')==True and os.path.isfile('x_hat_noisy_with_outliers.npy')==True):
    
    x_hat_noisy = np.load('x_hat_noisy.npy')
    x_hat_noisy_with_outliers = np.load('x_hat_noisy_with_outliers.npy')

  else:

    x_hat_noisy, x_hat_noisy_with_outliers = x_hat_create(data_y[:,:,:,:,0:N], r_squared_vec,del_t, time_t)
 
  len_r_vec = len(r_squared_vec)

  P_MSE_dB, P_sigma_dB = MSE(time_t, data_GT[:,:,:,0:N], data_y[:,0,:,:,0:N], data_y[:,1,:,:,0:N],
                              x_hat_noisy[:,:,:,0:N], x_hat_noisy_with_outliers[:,:,:,0:N], len_r_vec)
 
  print(P_MSE_dB.shape)
  plot_MSE(r_squared_vec_dB, P_MSE_dB, P_sigma_dB,scl,p)



     
if __name__ == "__main__":
    main()
 
