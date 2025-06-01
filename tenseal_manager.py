import tenseal as ts
import math

consts = {
    "1": 1.0,
    "2": 2.0,
    "1/2": 1/2,
    "1/6": 1/6,
    "1/8": 1/8,
    "1/16": 1/16,
    "1/24": 1/24,
    "1/120": 1/120,
    "3/40": 3/40,
    "pi_div_180": math.pi/180,
    "sqrt_c": [2.07154101e-02,  1.02939978e+01, -3.00582518e+02,  5.63080741e+03, -5.13503749e+04,  1.77884143e+05]
}

def create_ckks_context():
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=2**15,
        coeff_mod_bit_sizes=[
            60, 40, 40, 40, 40, 40, 
            40, 40, 40, 40, 40, 40,
            40, 40, 40, 40, 40, 40, 
            40, 60],
        encryption_type = ts.ENCRYPTION_TYPE.SYMMETRIC
    )
    context.global_scale = 2**40
    return context

def encrypt_constants(context):
    return  consts 
    """{
        key: ts.ckks_vector(context, [value])
        for key, value in consts.items()
    }"""

def encrypt_places(place1, place2, context):
    lon1 = ts.ckks_vector(context, [place1[0]])
    lat1 = ts.ckks_vector(context, [place1[1]])
    lon2 = ts.ckks_vector(context, [place2[0]])
    lat2 = ts.ckks_vector(context, [place2[1]])
    return (lon1, lat1), (lon2, lat2)
