class Mod2Polynomial:

    def __init__(self, vector):
        while len(vector) and not vector[-1]:
            vector.pop()
        self.vector = [0] * len(vector)
        i = 0
        for p in vector:
            self.vector[i] = int(bool(p))
            i += 1

    def __str__(self):
        def monomial_str(order):
            if order == 1:
                return "x"
            elif order > 0:
                return "x^{}".format(order)
            else:
                return "1"
        indexed_coefficients = zip(self.vector, range(0, len(self.vector)))
        polynomial_string = filter(bool, [monomial_str(o) if c else "" for c, o in indexed_coefficients])
        return " + ".join(polynomial_string) if polynomial_string else "0"

    def __add__(self, polynomial):
        size = max(self.get_order(), polynomial.get_order()) + 1
        a = self.vector + [0] * (size - len(self.vector))
        b = polynomial.vector + [0] * (size - len(polynomial.vector))
        return Mod2Polynomial([(ac + bc) % 2 for ac, bc in zip(a, b)])

    def __mul__(self, polynomial):
        if self.is_zero() or polynomial.is_zero():
            return Mod2Polynomial([])
        vector = [0] * (self.get_order() + polynomial.get_order() + 2)
        i1 = 0
        for p1 in self.vector:
            i2 = 0
            for p2 in polynomial.vector:
                vector[i1 + i2] = (vector[i1 + i2] + (p1 * p2)) % 2
                i2 += 1
            i1 += 1
        return Mod2Polynomial(vector)

    def __mod__(self, divisor):
        def make_monomial(n):
            vector = [0] * (n+1)
            vector[n] = 1
            return Mod2Polynomial(vector)
        dividend = Mod2Polynomial(self.vector[:])
        quotient = Mod2Polynomial([0] * (max(self.get_order(), divisor.get_order()) + 1))
        divisor_order = divisor.get_order()
        if not divisor_order:
            raise ZeroDivisionError
        while divisor_order <= dividend.get_order():
            monomial = make_monomial(dividend.get_order() - divisor_order)
            quotient += monomial
            dividend += (monomial * divisor)
        return dividend

    def get_order(self):
        i = 0
        order = 0
        for p in self.vector:
            if p: order = i
            i += 1
        return order

    def get_binary_representation(self, pad = 8):
        v = self.vector[:]
        v.reverse()
        return "".join([str(i) for i in v]).zfill(pad)

    def is_zero(self):
        return not any(self.vector)


for indexes in [[128, 7, 2, 1, 0], [96, 2, 0], [33, 32, 2]]:

    list = [0] * 129

    for el in indexes:
        list[128 - el] = 1

    print(list[::-1])


mod = Mod2Polynomial([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1][::-1])
a = Mod2Polynomial([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1][::-1])
b = Mod2Polynomial([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0][::-1])
print(a)
print(mod)
print(b)
print(a * b % mod)




print("e3 a6 b8 17 f2 0c 97 06 cf 6f e8 61 36 f9 47 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11".split(" ").__len__())


print("d4 b5 58 b0 6b 0a 2e 2c a5 fa ca 96 05 05 05 05".split(" ").__len__())

print("4d 27 d4 60 53 46 61 83 8d 1f ba 5e c2 5b e8 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10".split(" ").__len__())

print("c7 91 f0 7e 3f c4 7b 4f 29 f1 1b 72 aa 3f 5a 00".split(" ").__len__())

print("40 ae 38 55 f4 26 96 21 14 9d b8 e6 26 5c 01 01".split(" ").__len__())

print("b3 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f 0f".split(" ").__len__())
