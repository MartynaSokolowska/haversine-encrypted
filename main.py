from haversine_manager import haversine
from tenseal_manager import *

context = create_ckks_context()
enc_consts = encrypt_constants(context)

# (longitude, latitude)
lyon = (4.8422, 45.7597)   
paris = (2.3508, 48.8567)

lyon_enc, paris_enc = encrypt_places(lyon, paris, context)


dist = haversine(lyon[0], lyon[1], paris[0], paris[1], enc_consts)
print(dist)

enc_dist = haversine(
    lyon_enc[0], lyon_enc[1], paris_enc[0], paris_enc[1], enc_consts
)
print(enc_dist.decrypt())

