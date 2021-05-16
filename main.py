from typing import List, Union, Tuple
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd


class Curve:
    def __init__(self, coeffs: [float], name: str):
        self.__coeffs: [float] = coeffs
        self.__name: str = name

    def __str__(self) -> str:
        os = "Name: {}\n".format(self.__name)
        for c, i in enumerate(self.__coeffs):
            os += "({})x^({})".format(i, c)
            if c != len(self.__coeffs) - 1:
                os += " + "

        return os

    def value_at(self, x: float) -> float:
        res = 0.0
        for c, i in enumerate(self.__coeffs):
            res += pow(x, c) * i

        return res

    def __eq__(self, other) -> bool:
        return len(set(self.__coeffs).intersection(other.__coeffs)) == 0

    def __gt__(self, other) -> bool:
        return self.__coeffs[len(self.__coeffs)-1] > other.__coeffs[len(other.__coeffs)-1]

    def __lt__(self, other) -> bool:
        return self.__coeffs[len(self.__coeffs)-1] < other.__coeffs[len(other.__coeffs)-1]

    def normalize(self, inplace=False) -> Union["Curve", None]:
        h = self.__coeffs[len(self.__coeffs) - 1]
        if inplace:
            for i in self.__coeffs:
                i /= abs(h)
            return None
        else:
            return Curve([i/abs(h) for i in self.__coeffs], self.__name)


class IsLmModel:
    def __init__(self, i_s: Curve, l_m: Curve, dim: float = 1000.0):
        self.__dim = dim
        self.__i_s = i_s
        self.__l_m = l_m
        self.df = None

    def get_intersection(self) -> Union[Tuple[float, float], None]:
        err: float = 0.01
        step: float = 0.001
        i: float = 0.0
        while i <= self.__dim:
            i_s_val = self.__i_s.value_at(i)
            l_m_val = self.__l_m.value_at(i)
            if abs(i_s_val - l_m_val) <= err:
                return i, i_s_val

            i += step

        return None

    def plot(self, start: float = 0, end: float = 20) -> None:
        step: float = 0.01
        i: float = start
        if not self.df:
            is_vals: List[float] = []
            lm_vals: List[float] = []
            while i <= end:
                is_vals.append(self.__i_s.value_at(i))
                lm_vals.append(self.__l_m.value_at(i))
                i += step
            self.df = pd.DataFrame({"IS" : is_vals, "LM" : lm_vals})

        style.use("ggplot")
        plt.plot(self.df["IS"], label="IS")
        plt.plot(self.df["LM"], label="LM")
        plt.legend()
        plt.show()

    def i_s(self) -> Curve:
        return self.__i_s

    def l_m(self) -> Curve:
        return self.__l_m


if __name__ == '__main__':
    a = IsLmModel(Curve([10, -0.6], "IS").normalize(), Curve([0, 0.5], "LM").normalize())
    print(a.get_intersection())
    a.plot()