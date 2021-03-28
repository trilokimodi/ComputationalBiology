import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt
import pandas as pd
import os

cwd = os.getcwd()

beta = 5/8
alpha  = 1/4
gamma = 1/3
N = 10000
s_inf = list()
s_0 = np.arange(N)

class Q3d():
    def __init__(self, beta, betaL, betaM, betaS):
        self.beta = beta
        self.betaL = betaL
        self.betaM = betaM
        self.betaS = betaS
        self.alpha = 1/4
        self.gamma = 1/3
        self.delta = 1/10000
        self.s_0 = 1 - self.delta
        self.e_0 = self.delta
        self.i_0 = 0
        self.r_0 = 0
        self.remI = list()
        self.remR = list()
        self.no_preventive_solve()
        # self.plott()
        self.preventive_solve(self.betaL)
        # self.plott()
        self.preventive_solve(self.betaM)
        # self.plott()
        self.preventive_solve(self.betaS)
        # self.plott()
        self.pplot()
        self.pplot_r()

    def compute(self, y, t, alpha, beta, gamma):
        S, E, I, R = y
        self.ds = -beta * S * I
        self.de = beta * S*I - gamma *E
        self.di = gamma * E - alpha * I
        self.dr = alpha * I

        return [self.ds, self.de, self.di, self.dr]

    def no_preventive_solve(self):
        self.t = np.linspace(0, 255, 25500)
        self.solution = scipy.integrate.odeint(self.compute, [self.s_0, self.e_0, self.i_0, self.r_0], self.t, args=(self.alpha, self.beta, self.gamma))
        self.solution = np.array(self.solution)
        self.remI.append(self.solution[:, 2].copy())
        self.remR.append(self.solution[:, 3].copy())
        print(self.solution[-1,0]/self.s_0)

    def preventive_solve(self, betaNew):
        self.betaNew = betaNew
        self.t = np.linspace(0, 30, 3000)
        self.solution = scipy.integrate.odeint(self.compute, [self.s_0, self.e_0, self.i_0, self.r_0], self.t,
                                               args=(self.alpha, self.beta, self.gamma))
        self.solution = np.array(self.solution)
        self.plotDataFrame = pd.DataFrame(self.solution, columns=None)

        self.t = np.linspace(30, 130, 10000)
        self.solution = scipy.integrate.odeint(self.compute, [self.solution[-1, 0], self.solution[-1, 1], self.solution[-1, 2], self.solution[-1, 3]], self.t,
                                               args=(self.alpha, self.betaNew, self.gamma))
        self.solution = np.array(self.solution)
        self.plotDataFrame = self.plotDataFrame.append(pd.DataFrame(self.solution, columns=None))

        self.t = np.linspace(130, 255, 12500)
        self.solution = scipy.integrate.odeint(self.compute,
                                               [self.solution[-1, 0], self.solution[-1, 1], self.solution[-1, 2],
                                                self.solution[-1, 3]], self.t,
                                               args=(self.alpha, self.beta, self.gamma))
        self.solution = np.array(self.solution)
        self.plotDataFrame = self.plotDataFrame.append(pd.DataFrame(self.solution, columns=None))

        self.solution = self.plotDataFrame.to_numpy()
        self.t = np.linspace(0, 255, 25500)

        self.remI.append(self.solution[:, 2].copy())
        self.remR.append(self.solution[:, 3].copy())


    # def plott(self):
    #     plt.figure()
    #     plt.plot(self.t, self.solution[:, 0], label="S(t)")
    #     plt.plot(self.t, self.solution[:, 1], label="E(t)")
    #     plt.plot(self.t, self.solution[:, 2], label="I(t)")
    #     plt.plot(self.t, self.solution[:, 3], label="R(t)")
    #     plt.legend()
    #     plt.show()

    def pplot(self):
        plt.figure()
        figNameP = cwd + "\\EXAM_Q3d_I.png"
        plt.plot(self.t, self.remI[0], label="No")
        plt.plot(self.t, self.remI[1], label="Light")
        plt.plot(self.t, self.remI[2], label="Moderate")
        plt.plot(self.t, self.remI[3], label="Severe")
        plt.legend()
        plt.xlabel("time steps")
        plt.ylabel("Fraction of infected")
        plt.title("Infected comparison")
        plt.savefig(figNameP)

    def pplot_r(self):
        plt.figure()
        figNameP = cwd + "\\EXAM_Q3d_R.png"
        plt.plot(self.t, self.remR[0], label="No")
        plt.plot(self.t, self.remR[1], label="Light")
        plt.plot(self.t, self.remR[2], label="Moderate")
        plt.plot(self.t, self.remR[3], label="Severe")
        plt.legend()
        plt.xlabel("time steps")
        plt.ylabel("Fraction of Recovered")
        plt.title("Recovered comparison")
        plt.savefig(figNameP)

obj = Q3d(5/8, 1/2, 3/8, 1/3)
