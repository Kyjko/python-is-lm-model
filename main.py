from is_lm_model import IsLmModel, Curve
from deficit_model import DeficitModel

if __name__ == '__main__':
    a = IsLmModel(Curve([10, -0.6], "IS").normalize(), Curve([0, 0.5], "LM").normalize())
    print(a.get_intersection())
    a.plot()

    d = DeficitModel(0.05, 0.03, 0.8, 0.05, 0.02)
    d.simulate(10)
    print(d)
    d.print()