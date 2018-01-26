from lib601.poly import Polynomial

class System:
    def simulator(self):
        return SystemSimulator(self)

    def poles(self):
        # Find the poles of a system functional by substituting
        # 1/z for R in both numerator and denominator, and then
        # finding the roots of the denominator polynomial of z.

        # We can find the coefficients of the z polynomial by reversing the
        # order of the coefficients of the R polynomial.
        # However, we must make the numerator and denominator coefficient lists
        # have the same length (by padding with zeros) to avoid introducing
        # false roots (at zero).

        # create equal-length lists of coefficients corresponding to polynomials in z
        num = []
        den = []
        for i in range(max(self.numerator.order,self.denominator.order), -1, -1):
            num.append(self.numerator.coeff(i))
            den.append(self.denominator.coeff(i))
        # cancel poles at zero with zeros at zero
        while len(num) > 0 and num[0]==den[0]==0:
            num.pop(0)
            den.pop(0)
        return Polynomial(den).roots()

    def dominant_pole(self):
        p = self.poles()
        if len(p) == 0:
            return None
        return max(p, key=abs)


class SystemSimulator:
    def __init__(self, system):
        self.system = system
        self.reset()

    def step(self, inp):
        new_state, out = self.system.calculate_step(self.state, inp)
        self.state = new_state
        return out

    def reset(self):
        self.state = self.system.initial_state

    def get_response(self, inputs, reset=True):
        if reset:
            self.reset()
        return [self.step(inp) for inp in inputs]


class R(System):
    def __init__(self, output0=0):
        self.initial_state = output0
        self.numerator = Polynomial([0, 1])
        self.denominator = Polynomial([1])

    def calculate_step(self, state, inp):
        out = state
        state = inp
        return (state, out)


class Gain(System):
    def __init__(self, k):
        self.initial_state = None
        self.k = k
        self.numerator = Polynomial([k])
        self.denominator = Polynomial([1])

    def calculate_step(self, state, inp):
        out = self.k * inp
        return (state, out)


class Cascade(System):
    def __init__(self, s1, s2):
        self.initial_state = (s1.initial_state, s2.initial_state)
        self.s1 = s1
        self.s2 = s2
        self.numerator = s1.numerator * s2.numerator
        self.denominator = s1.denominator * s2.denominator

    def calculate_step(self, state, inp):
        s1_state, s2_state = state
        s1_state, intermediate = self.s1.calculate_step(s1_state, inp)
        s2_state, out = self.s2.calculate_step(s2_state, intermediate)
        state = (s1_state, s2_state)
        return (state, out)


class FeedforwardAdd(System):
    def __init__(self, s1, s2):
        self.initial_state = (s1.initial_state, s2.initial_state)
        self.s1 = s1
        self.s2 = s2

        n1, d1 = self.s1.numerator, self.s1.denominator
        n2, d2 = self.s2.numerator, self.s2.denominator
        self.numerator = n1*d2 + n2*d1
        self.denominator = d1*d2

    def calculate_step(self, state, inp):
        s1_state, s2_state = state
        s1_state, out1 = self.s1.calculate_step(s1_state, inp)
        s2_state, out2 = self.s2.calculate_step(s2_state, inp)
        state = (s1_state, s2_state)
        out = out1 + out2
        return (state, out)


class FeedbackAdd(System):
    def __init__(self, s1, s2):
        self.initial_state = (s1.initial_state, s2.initial_state)
        self.s1 = s1
        self.s2 = s2

        n1, d1 = self.s1.numerator, self.s1.denominator
        n2, d2 = self.s2.numerator, self.s2.denominator
        self.numerator = n1*d2
        self.denominator = d1*d2 - n1*n2

    def calculate_step(self, state, inp):
        s1_state, s2_state = state

        s1_state_hyp, out1_hyp = self.s1.calculate_step(s1_state, inp)
        s2_state_hyp, out2_hyp = self.s2.calculate_step(s2_state, out1_hyp)

        out2_real = out2_hyp

        s1_state_real, out1_real = self.s1.calculate_step(s1_state, inp + out2_real)
        s2_state_real, out2_real = self.s2.calculate_step(s2_state, out1_real)

        state = (s1_state_real, s2_state_real)
        out = out1_real

        return (state, out)
