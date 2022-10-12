def call_data():

  data_GT = np.loadtxt('/content/groundtruth_2013-04-05.csv', delimiter = ",")
  time_GT = (data_GT[:, 0] - data_GT[0, 0]) * 1e-6
  data_GPS = np.loadtxt('/content/gps_2013-04-05.csv', delimiter = ",")
  time_GPS = (data_GPS[:, 0] - data_GPS[0, 0]) * 1e-6

  def calculate(data):
    lat = data[:, 3]
    lng = data[:, 4]
    alt = data[:, 5]

    lat0 = lat[0]
    lng0 = lng[0]

    dLat = lat - lat0
    dLng = lng - lng0

    r = 6400000 # approx. radius of earth (m)
    x = r * np.cos(lat0) * np.sin(dLng)
    y = r * np.sin(dLat)
    data = np.concatenate((np.expand_dims(x, axis=1), np.expand_dims(y, axis=1)), axis=1)

    return data.transpose()

  data_GPS_x = calculate(data_GPS)[1, :]
  data_GPS_y = calculate(data_GPS)[0, :]

  GT_x = data_GT[:, 1] - data_GT[1, 1]
  GT_y = data_GT[:, 2] - data_GT[1, 2]

  data_GT_x = np.interp(time_GPS, time_GT, GT_x)
  data_GT_y = np.interp(time_GPS, time_GT, GT_y)
   
  return data_GT_x, data_GT_y, data_GPS_x, data_GPS_y, time_GPS, time_GT
