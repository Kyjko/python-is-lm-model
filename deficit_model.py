from typing import Union


class DeficitModel:
    def __init__(self, gamma: float, tau: float, delta0: float, r: float, g: float):
        self.__gamma: float = gamma
        self.__tau: float = tau
        self.__delta0: float = delta0
        self.__r: float = r
        self.__g: float = g
        self.deltas: [float] = [self.__delta0]
        self.__error: str = ""


    def __str__(self):
        os: str = "Growth: {}\nInitial debt: {}\nTaxes: {}\nInterest rate: {}\nGovernment spending: {}\n".\
                format(self.__g, self.__delta0, self.__tau, self.__r, self.__gamma)

        if self.__r > self.__g:
            os += "The model is asymptotically unstable"
        else:
            os += "The model is asymptotically stable"

        return os

    def simulate(self, n: int) -> None:
        for i in range(n):
            delta = self.deltas[-1]*(1+self.__r)/(1+self.__g) + (self.__gamma-self.__tau)/(1+self.__g)
            self.deltas.append(delta)

    def stable(self) -> Union[float, str]:
        try:
            return (self.__tau - self.__gamma) / (self.__r - self.__g)
        except ZeroDivisionError:
            self.__error = "Cannot determine stable delta!"
            return "{} > {}".format(hash((self.__error, 1)), self.__error)

    def print(self) -> None:
        os = "Deltas:\n"
        for i in self.deltas:
            os += "{}\n".format(str(i))

        print(os)
