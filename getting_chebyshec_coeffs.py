import numpy as np
from numpy.polynomial.chebyshev import Chebyshev

x_vals = np.linspace(0, 0.1, 100)
y_vals = np.sqrt(x_vals)

cheb = Chebyshev.fit(x_vals, y_vals, deg=5, domain=[0, 0.1])
poly = cheb.convert(kind=np.polynomial.Polynomial)

print("coeffs:", poly.coef)