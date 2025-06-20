from encrypted_functions import *
import gc

def enc_haversine(lon1, lat1, lon2, lat2, enc_consts):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    calculator = EncryptedFunctions(enc_consts)
    enc_const_1_2 = enc_consts["1/2"]
    
    lon1 = calculator.enc_radians(lon1)
    lat1 = calculator.enc_radians(lat1)
    lon2 = calculator.enc_radians(lon2)
    lat2 = calculator.enc_radians(lat2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    del lon1, lon2
    gc.collect()

    sin_dlat = calculator.enc_sin(dlat*enc_const_1_2)
    sin_dlat_sq = sin_dlat * sin_dlat
    del sin_dlat, dlat
    gc.collect()
    
    sin_dlon = calculator.enc_sin(dlon*enc_const_1_2)
    sin_dlon_sq = sin_dlon * sin_dlon
    del sin_dlon, dlon
    gc.collect()
    
    cos_lat1 = calculator.enc_cos(lat1)
    cos_lat2 = calculator.enc_cos(lat2)
    del lat1, lat2
    gc.collect()
    
    a = sin_dlat_sq + (cos_lat1 * cos_lat2 * sin_dlon_sq)
    del sin_dlat_sq, sin_dlon_sq, cos_lat1, cos_lat2
    gc.collect()
    # print("a: ", a.decrypt()[0])

    # Scale the input 'a' before applying the sqrt approximation.
    # This improves numerical stability of the Chebyshev approximation.
    # The approximation is designed for inputs in [1e-5, 1.5e-2] (from 0 to 1km), so we scale:
    # - a * 1e6 to move the original domain [1e-11, 1.5e-8] → [1e-5, 1.5e-2]
    # - After sqrt approximation, scale back by multiplying with 1e-3.
    # This approach ensures reasonable accuracy for close distances.
    scaled_a = a * 1e6
    sqrt_a = calculator.enc_sqrt(scaled_a)
    sqrt_a = sqrt_a * 1e-3
    del a
    gc.collect()

    asin_val = calculator.enc_asin(sqrt_a)
    del sqrt_a
    gc.collect()

    enc_const_2 = enc_consts["2"]
    c = enc_const_2 * asin_val
    del asin_val
    gc.collect()

    r = 6371 
    return c * r