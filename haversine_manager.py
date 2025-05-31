from encrypted_functions import *
import gc

def haversine(lon1, lat1, lon2, lat2, enc_consts, iterations=3):
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

    # print("lon1, lat1, lon2, lat2: ", lon1.decrypt()[0], lat1.decrypt()[0], lon2.decrypt()[0], lat2.decrypt()[0])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # print("dlon, dlat: ", dlon.decrypt()[0], dlat.decrypt()[0])

    del lon1, lon2
    gc.collect()

    sin_dlat = calculator.enc_sin(dlat*enc_const_1_2)
    # print("sin dlat ", sin_dlat.decrypt()[0])
    sin_dlat_sq = sin_dlat * sin_dlat
    # print("sin dlat sq ", sin_dlat_sq.decrypt()[0])
    del sin_dlat, dlat
    gc.collect()

    
    sin_dlon = calculator.enc_sin(dlon*enc_const_1_2)
    # print("sin dlon ", sin_dlon.decrypt()[0])
    sin_dlon_sq = sin_dlon * sin_dlon
    # print("sin dlon sqrt ", sin_dlon_sq.decrypt()[0])
    del sin_dlon, dlon
    gc.collect()
    
    
    cos_lat1 = calculator.enc_cos(lat1)
    # print("cos lat1 ", cos_lat1.decrypt()[0])
    cos_lat2 = calculator.enc_cos(lat2)
    # print("cos lat2 ", cos_lat2.decrypt()[0])

    del lat1, lat2
    gc.collect()
    
    a = sin_dlat_sq + (cos_lat1 * cos_lat2 * sin_dlon_sq)
    # print("a: ", a.decrypt()[0])
    del sin_dlat_sq, sin_dlon_sq, cos_lat1, cos_lat2
    gc.collect()

    scaled_a = a * 1e4
    sqrt_a = calculator.enc_sqrt(scaled_a)
    sqrt_a = sqrt_a * 1e-2
    # print("sqrt a: ", sqrt_a.decrypt()[0])
    del a
    gc.collect()

    asin_val = calculator.enc_asin(sqrt_a)
    # print("asin ", asin_val.decrypt()[0])
    del sqrt_a
    gc.collect()

    enc_const_2 = enc_consts["2"]
    c = enc_const_2 * asin_val
    # print("c ", c.decrypt()[0])

    del asin_val
    gc.collect()

    r = 6371 
    return c * r