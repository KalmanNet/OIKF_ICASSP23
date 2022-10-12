def plot_MSE(data_y, x_hat, time, P_MSE_dB, P_MSE_m, index_vec):

  plt.figure(figsize=(9, 6))
  plt.plot(time/60, (data_y), color='orange', linewidth=2, label="GPS Measurements")
  plt.plot(time/60, (x_hat[3,0,:,int(index_vec[3,0]), int(index_vec[3,1])]), 'g--', linewidth=2, label='OIKF-AM')

  plt.ylabel('Position [m]', size='18')
  plt.xlabel("Time [min]", size='18')
  plt.grid()
  plt.xticks(size=14)
  plt.yticks(size=14)
  plt.legend(fontsize='14')
  plt.savefig('position_filters.pdf', bbox_inches='tight')
  plt.show()

  ############################################################
  def int2str(time):
    return str(np.round(time, 2))

  table = [[ "",                 "RMSE[m]",    " MSE[dB]",                               ], 
          ['Noise floor', int2str(P_MSE_m[5, int(index_vec[5, 0]), int(index_vec[5, 1])]),  int2str(P_MSE_dB[5, int(index_vec[5, 0]),int(index_vec[5, 1])])],  
          ['KF',          int2str(P_MSE_m[0, int(index_vec[0, 0]), int(index_vec[0, 1])]),  int2str(P_MSE_dB[0, int(index_vec[0, 0]),int(index_vec[0, 1])])],    
          ['ORKF',      int2str(P_MSE_m[1, int(index_vec[1, 0]), int(index_vec[1, 1])]),  int2str(P_MSE_dB[1, int(index_vec[1, 0]),int(index_vec[1, 1])])], 
          ['Chi-squared', int2str(P_MSE_m[2, int(index_vec[2, 0]), int(index_vec[2, 1])]),  int2str(P_MSE_dB[2, int(index_vec[2, 0]),int(index_vec[2, 1])])],
          ['OIKF-AM',     int2str(P_MSE_m[3, int(index_vec[3, 0]), int(index_vec[3, 1])]),  int2str(P_MSE_dB[3, int(index_vec[3, 0]),int(index_vec[3, 1])])],
          ['OIKF-EM',     int2str(P_MSE_m[4, int(index_vec[4, 0]), int(index_vec[4, 1])]),  int2str(P_MSE_dB[4, int(index_vec[4, 0]),int(index_vec[4, 1])]),]]

  print(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign='center'))
  with open('Tab_MSE.txt', 'w') as f:
    f.write(tabulate(table, headers='firstrow', tablefmt='latex', numalign='center'))
  f.close()
