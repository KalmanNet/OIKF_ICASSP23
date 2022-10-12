
import numpy as np
from scipy.stats import bernoulli,rayleigh
def create_GT(N, q_squared_vec, len_q_vec, del_t, time_t):

    data_GT = np.zeros((2, len(time_t), len(q_squared_vec), N))

    for n in range(N):
        for q in range(len_q_vec):
            q_squared = np.array([[1], [1]]) * q_squared_vec[q]
            for t in range(1, len(time_t)):
                F = np.array([[1, del_t], [0, 1]])
                Q = np.array([[(1 / 3) * (del_t ** 3), (1 / 2) * (del_t ** 2)], [(1 / 2) * (del_t ** 2), (del_t)]]) * q_squared
                e_t = np.random.multivariate_normal([0,0], Q)
                data_GT[:, t:t+1, q, n] = F @ data_GT[:, t-1:t, q, n] + np.expand_dims(e_t, axis=1)

    return data_GT


def main():
    N = 2
    end_time = 10
    del_t = 1e-1
    time_t = np.linspace(0, end_time, int(end_time / del_t) + 1)
    q_squared_vec = np.array((1e-1, 1, 1e1))
    r_squared_vec = np.array((1e1, 1, 1e-1, 1e-2, 1e-3))
    len_r_vec = len(r_squared_vec)
    len_q_vec = len(q_squared_vec)

    #### ground truth ########
    data_GT = create_GT(N, q_squared_vec, len_q_vec, del_t, time_t)
    file_name_GT = 'CV/data_GT'
    np.save(file_name_GT, data_GT)

    #### signal of ovseravations ########
    data_y = np.zeros((data_GT.shape[0], data_GT.shape[1], len_r_vec, len_q_vec, N))

    p = 0.2
    scl = 30
    for n in range(N):

        for r in range(len_r_vec):

            for q in range(len_q_vec):
                outliers_pos = bernoulli.rvs(p, size=len(time_t))
                index_pos = np.where(outliers_pos == 1)[0]
                ray_pos = rayleigh.rvs(size=len(index_pos), scale=scl)
                data_y[0, index_pos, r, q, n] = data_GT[0, index_pos, q, n] + ray_pos

                outliers_vel = bernoulli.rvs(p, size=len(time_t))
                index_vel = np.where(outliers_vel == 1)[0]
                ray_vel = rayleigh.rvs(size=len(index_vel), scale=scl)

                data_y[1, index_vel, r, q, n] = data_GT[1, index_vel, q, n] + ray_vel

    file_name_data_y = 'CV/data_y'
    np.save(file_name_data_y, data_y)


if __name__ == "__main__":
    main()
