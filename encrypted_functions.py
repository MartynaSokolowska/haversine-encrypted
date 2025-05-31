import numpy as np
from numpy.polynomial.chebyshev import Chebyshev

class EncryptedFunctions():
    def __init__(self, enc_consts):
        self.enc_consts = enc_consts

    def enc_sin(self, enc_x):
        enc_const_1_6 = self.enc_consts["1/6"]
        x2 = enc_x * enc_x
        x3 = x2 * enc_x

        return enc_x - x3 * enc_const_1_6

    def enc_cos(self, enc_x):
        enc_const_1 = self.enc_consts["1"] 
        enc_const_1_24 = self.enc_consts["1/24"] 
        enc_const_1_2 = self.enc_consts["1/2"] 
        x2 = enc_x * enc_x
        x4 = x2 * x2

        return enc_const_1 - x2 * enc_const_1_2 + x4 * enc_const_1_24

    def enc_sqrt(self, enc_x):
        coeffs = self.enc_consts["sqrt_c"]

        c0 = coeffs[0]
        c1 = coeffs[1]
        c2 = coeffs[2]
        c3 = coeffs[3]
        c4 = coeffs[4]
        c5 = coeffs[5]

        x2 = enc_x * enc_x
        x3 = x2 * enc_x
        x4 = x2 * x2
        x5 = x4 * enc_x

        return c0 + enc_x*c1 + x2*c2 + x3*c3 + x4*c4 + x5*c5
    
    def enc_asin(self, enc_x):
        enc_const_1_6 = self.enc_consts["1/6"]
        x2 = enc_x * enc_x
        x3 = x2 * enc_x
        return enc_x + x3 * enc_const_1_6

    def enc_radians(self, enc_latlon_deg):
        enc_pi_div_180 = self.enc_consts["pi_div_180"]
        return enc_latlon_deg * enc_pi_div_180
        
