# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from abc import ABC

import numpy as np

ADD = 0.2
MINUS = ADD/2


class LearnStrategy(ABC):
    def learn(self, plus, minus1, minus2): pass
    def getState(self): pass


class States(ABC):
    t1 = ['P', 'K', 'N']

    #          P        K       N
    p_t1 = [[1 / 3, 1 / 3, 1 / 3],  # P
            [1 / 3, 1 / 3, 1 / 3],  # K
            [1 / 3, 1 / 3, 1 / 3]]  # N

    def check(self, plus, minus1, minus2, wiersz):
        max = self.p_t1[wiersz][plus] + ADD <= 1
        min1 = self.p_t1[wiersz][minus1] - MINUS >= 0
        min2 = self.p_t1[wiersz][minus2] - MINUS >= 0
        ok = max and min1 and min2
        if ok:
            print("uczę się")
        else:
            print("Jestem na", np.round(self.p_t1[wiersz][plus] * 100, 1), "% pewien, że po ", self.t1[wiersz],"muszę zagrać", self.t1[plus])
        return ok


class ScissorsLearnStrategy(LearnStrategy, States):
    def learn(self, plus, minus1, minus2):
        if self.check(plus, minus1, minus2, 2):
            self.p_t1[2][plus] += ADD
            self.p_t1[2][minus1] -= MINUS
            self.p_t1[2][minus2] -= MINUS

    def getState(self):
        return np.random.choice(self.t1, p=self.p_t1[2])


class StoneLearnStrategy(LearnStrategy, States):
    def learn(self, plus, minus1, minus2):
        if self.check(plus, minus1, minus2, 1):
            self.p_t1[1][plus] += ADD
            self.p_t1[1][minus1] -= MINUS
            self.p_t1[1][minus2] -= MINUS

    def getState(self):
        return np.random.choice(self.t1, p=self.p_t1[1])


class PaperLearnStrategy(LearnStrategy, States):
    def learn(self, plus, minus1, minus2):
        if self.check(plus, minus1, minus2, 0):
            self.p_t1[0][plus] += ADD
            self.p_t1[0][minus1] -= MINUS
            self.p_t1[0][minus2] -= MINUS

    def getState(self):
        return np.random.choice(self.t1, p=self.p_t1[0])


class HMMComponent(States):

    def __init__(self, learnStrategy):
        self.learnStrategy = learnStrategy

    def learnStateMatrix(self, plus, minus1, minus2):
        return self.learnStrategy.learn(self, plus, minus1, minus2)

    def getStateMatrix(self):
        return self.learnStrategy.getState(self)


def main():
    myChoices = ['K', 'P', 'P', 'N', 'K', 'P', 'K', 'P', 'N', 'N', 'K', 'K', 'P', 'P', 'N', 'N', 'K', 'P', 'K', 'P','N', 'K', 'N', 'K', 'P']
    # myChoices = ['K', 'K', 'K', 'K', 'K', 'K', 'K', 'K', "K", 'K', 'K', 'K', 'K', 'K']

    win = 0
    i = 0

    for st in myChoices:
        i += 1
        if st == 'K':
            state = HMMComponent(StoneLearnStrategy).getStateMatrix()
            HMMComponent(StoneLearnStrategy).learnStateMatrix(0, 1, 2)
            if state == 'P':
                win += 1  # komputer wygrywa
            elif state == 'N':
                win -= 1  # komputer przegrywa
        elif st == 'P':
            state = HMMComponent(PaperLearnStrategy).getStateMatrix()
            HMMComponent(PaperLearnStrategy).learnStateMatrix(2, 0, 1)
            if state == 'N':
                win += 1
            elif state == 'K':
                win -= 1
        elif st == 'N':
            state = HMMComponent(ScissorsLearnStrategy).getStateMatrix()
            HMMComponent(ScissorsLearnStrategy).learnStateMatrix(1, 0, 2)
            if state == 'K':
                win += 1
            elif state == 'P':
                win -= 1
        print("  P    ", "K    ", "N")
        print(np.round(States.p_t1, 2))
        print("Mój wybór", st)
        print("Wybór komputera", state)
        print("wygrane komputera na", i, "gier", win)
        print("\n")
        # time.sleep(0.5)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
