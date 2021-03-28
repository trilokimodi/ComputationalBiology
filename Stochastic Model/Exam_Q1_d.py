import numpy as np
import matplotlib.pyplot as plt
import os
MAX_REALIZATIONS = 1
MAX_ITER = 50000

dt = 0.01
b = 0.1
p = 1
K = 500

class Q1d():
    def __init__(self, p, N_0):
        self.b = 0.1
        self.p = p
        self.n = [N_0]
        self.dt = 0.01
        self.K = 500
        self.p_bn = self.b * self.dt
        self.find_t()
        self.compute_avg()

    def find_t(self):
        for iIter in range(MAX_ITER):
            self.tempPop = 0
            for iPop in range(self.n[-1]):
                self.rand_prob = np.random.random()
                if self.rand_prob <= self.p_bn * (1 - (self.n[-1]/self.K)):
                    if np.random.random() <= self.p:
                        self.tempPop += 1
            self.n.append(self.n[-1] + self.tempPop)

    def compute_avg(self):
        self.avg = sum(self.n) / np.sum(dt * np.arange(len(self.n) - 1))


for iN in [1, 10, 100]:

    populations = list()
    average = list()

    for iRealization in range(MAX_REALIZATIONS):
        g1 = Q1d(p, iN)
        populations.append(g1.n)
        average.append(g1.avg)

    prac_average = (sum(average)) / MAX_REALIZATIONS

    theor = list()
    for t in range(MAX_ITER):
        num = iN * K * np.exp(b * t * dt)
        den = iN * (np.exp(b * t * dt) - 1) + K
        theor.append(num/den)
    theory_average = sum(theor) / (dt * MAX_ITER * (MAX_ITER + 1) / 2)

    two_rand_realization = np.random.randint(0, MAX_REALIZATIONS, 2)

    cwd = os.getcwd()
    figNameP = cwd + "\\EXAM_Q1d_N_" + str(iN) + ".png"
    plt.figure()
    plt.xlabel("time")
    plt.ylabel("log(population)")
    plt.title("p = {0}, real = {1}, s_avg = {2:.2f}, t_avg = {3:.2f}".format(p, MAX_REALIZATIONS, prac_average, theory_average))
    plt.plot(np.log(np.array(populations[two_rand_realization[0]])), color="blue", label=f"realization {two_rand_realization[0]}")
    plt.plot(np.log(np.array(populations[two_rand_realization[1]])), color="red", label=f"realization {two_rand_realization[1]}")
    plt.plot(np.log(np.array(theor)), color="green", label="Deterministic")
    plt.legend()
    plt.show()
    # plt.savefig(figNameP)

