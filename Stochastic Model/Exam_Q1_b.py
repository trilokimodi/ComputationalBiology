import numpy as np
import matplotlib.pyplot as plt
import os
MAX_REALIZATIONS = 100
MAX_ITER = 10000

dt = 0.01
N_0 = 1
b = 0.1
p = [0.5, 1]
class Gillespie():
    def __init__(self, p, dt, N_0, b):
        self.p = p
        self.b = b
        self.N = [N_0]
        self.t = [0]
        self.dt = dt
        self.pb = self.dt * self.b
        self.find_t()
        self.compute_avg()

    def find_t(self):
        while True:
            rand_expo = int(np.min(np.floor(np.random.exponential(scale=1/self.pb, size=self.N[-1]))))
            self.N += [self.N[-1]] * rand_expo
            rand_p = np.random.random()
            if rand_p <= self.p:
                self.N.append(self.N[-1] + 1)
            else:
                self.N.append(self.N[-1] + 2)
            if len(self.N) > MAX_ITER:
                break

    def compute_avg(self):
        self.avg = sum(self.N)/np.sum(dt * np.arange(len(self.N) - 1))


for iP in p:
    populations = list()
    average = list()

    for iRealization in range(MAX_REALIZATIONS):
        g1 = Gillespie(iP, dt, N_0, b)
        populations.append(g1.N)
        average.append(g1.avg)

    prac_average = (sum(average))/MAX_REALIZATIONS

    theor = list()
    for t in range(MAX_ITER):
        theor.append(N_0 * np.exp(b * (2 - iP) * t * dt))
    tt = dt * np.arange(MAX_ITER)
    # theory_average = N_0 * np.exp(b * (2 - iP) * MAX_ITER * dt)
    theory_average = sum(theor)/np.sum(tt)

    two_rand_realization = np.random.randint(0, MAX_REALIZATIONS, 2)
    cwd = os.getcwd()
    figNameP = cwd + "\\EXAM_Q1b_p_" + str(iP*10) + ".png"
    plt.figure()
    plt.xlabel("time steps")
    plt.ylabel("log(population)")
    plt.title("p = {0}, Real = {1}, S_avg = {2:.2f}, T_avg = {3:.2f}".format(iP, MAX_REALIZATIONS, prac_average, theory_average))
    plt.plot(np.log(np.array(populations[two_rand_realization[0]])), color="blue", label=f"realization {two_rand_realization[0]}")
    plt.plot(np.log(np.array(populations[two_rand_realization[1]])), color="red", label=f"realization {two_rand_realization[1]}")
    plt.legend()
    # plt.show()
    plt.savefig(figNameP)

# plt.figure()
# theor = list()
# for t in range(MAX_ITER):
#     theor.append(N_0 * np.exp(b * (2 - p[0]) * t * dt))
# print(sum(theor)/(dt * MAX_ITER * (MAX_ITER + 1)/2))
# plt.plot(np.array(theor))
# plt.show()
