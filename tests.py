import unittest
import math
import tenseal as ts
from encrypted_functions import EncryptedFunctions
from haversine_manager import enc_haversine
from tenseal_manager import create_ckks_context, encrypt_constants, encrypt_places, consts
from haversine import haversine, Unit


class TestEncryptedFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = create_ckks_context()
        cls.consts = encrypt_constants(cls.context)
        cls.calc = EncryptedFunctions(cls.consts)

    def decrypt(self, vector):
        return vector.decrypt()[0]

    def test_enc_sin(self):
        for x in [-0.5, 0, 0.5]:
            with self.subTest(x=x):
                enc_x = ts.ckks_vector(self.context, [x])
                result = self.calc.enc_sin(enc_x)
                decrypted = self.decrypt(result)
                expected = math.sin(x)
                self.assertAlmostEqual(decrypted, expected, delta=0.01)

    def test_enc_cos(self):
        for x in [-0.5, 0, 0.5]:
            with self.subTest(x=x):
                enc_x = ts.ckks_vector(self.context, [x])
                result = self.calc.enc_cos(enc_x)
                decrypted = self.decrypt(result)
                expected = math.cos(x)
                self.assertAlmostEqual(decrypted, expected, delta=0.01)

    def test_enc_sqrt(self):
        for x in [1e-09, 1e-10]: 
            with self.subTest(x=x):
                enc_x = ts.ckks_vector(self.context, [x])
                scaled_x = enc_x*1e6
                result = self.calc.enc_sqrt(scaled_x)
                result = result * 1e-3
                decrypted = self.decrypt(result)
                expected = math.sqrt(x)
                self.assertAlmostEqual(decrypted, expected, delta=0.01)

    def test_enc_asin(self):
        for x in [-0.5, 0, 0.5]: 
            with self.subTest(x=x):
                enc_x = ts.ckks_vector(self.context, [x])
                result = self.calc.enc_asin(enc_x)
                decrypted = self.decrypt(result)
                expected = math.asin(x)
                self.assertAlmostEqual(decrypted, expected, delta=0.01)

    def test_enc_radians(self):
        for deg in [0, 45, 90]:
            with self.subTest(deg=deg):
                enc_deg = ts.ckks_vector(self.context, [deg])
                result = self.calc.enc_radians(enc_deg)
                decrypted = self.decrypt(result)
                expected = math.radians(deg)
                self.assertAlmostEqual(decrypted, expected, delta=0.0001)

    def test_enc_sin_squared(self):
        for x in [-0.5, 0.0, 0.5]:
            with self.subTest(x=x):
                enc_x = ts.ckks_vector(self.context, [x])
                sin_enc = self.calc.enc_sin(enc_x)
                sin2_enc = sin_enc * sin_enc
                decrypted = self.decrypt(sin2_enc)
                expected = math.sin(x) ** 2
                self.assertAlmostEqual(decrypted, expected, delta=0.01)

                                
class TestEncryptedHaversine(unittest.TestCase):
    def test_enc_haversine_multiple_cases(self):
        context = create_ckks_context()

        test_cases = [
            # format: ((lon1, lat1), (lon2, lat2), ≈distance_km)
            ((21.000000, 52.000000), (21.000000, 52.000090)),  # ~10 m
            ((21.000000, 52.000000), (21.000000, 52.001078)),  # ~120 m
            ((21.000000, 52.000000), (21.000000, 52.002066)),  # ~230 m
            ((21.000000, 52.000000), (21.000000, 52.003054)),  # ~340 m
            ((21.000000, 52.000000), (21.000000, 52.004042)),  # ~450 m
            ((21.000000, 52.000000), (21.000000, 52.005031)),  # ~560 m
            ((21.000000, 52.000000), (21.000000, 52.006019)),  # ~670 m
            ((21.000000, 52.000000), (21.000000, 52.007007)),  # ~780 m
            ((21.000000, 52.000000), (21.000000, 52.007995)),  # ~890 m
            ((21.000000, 52.000000), (21.000000, 52.008983)),  # ~1000 m (1 km)
        ]

        for place1, place2 in test_cases:
            with self.subTest(place1=place1, place2=place2):
                (enc_lon1, enc_lat1), (enc_lon2, enc_lat2) = encrypt_places(place1, place2, context)
                enc_result = enc_haversine(enc_lon1, enc_lat1, enc_lon2, enc_lat2, consts)
                decrypted = enc_result.decrypt()[0]

                expected = haversine(place1[::-1], place2[::-1], unit=Unit.KILOMETERS)

                print(f"Encrypted: {decrypted:.6f} km, Expected: {expected:.6f} km")
                self.assertAlmostEqual(decrypted, expected, delta=0.005)

        def plain_haversine(lon1, lat1, lon2, lat2):
            lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            return 6371 * c


if __name__ == '__main__':
    unittest.main()
