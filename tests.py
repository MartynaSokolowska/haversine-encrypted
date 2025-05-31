import unittest
import math
import tenseal as ts
from encrypted_functions import EncryptedFunctions
from haversine_manager import haversine
from tenseal_manager import create_ckks_context, encrypt_constants, encrypt_places, consts



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
        for x in [0.01, 0.05, 0.09]: 
            with self.subTest(x=x):
                enc_x = ts.ckks_vector(self.context, [x])
                result = self.calc.enc_sqrt(enc_x)
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
    def test_enc_haversine(self):
        context = create_ckks_context()

        place1 = (4.8422, 45.7597)         
        place2 = (2.3508, 48.8567) 
        (enc_lon1, enc_lat1), (enc_lon2, enc_lat2) = encrypt_places(place1, place2, context)

        enc_result = haversine(enc_lon1, enc_lat1, enc_lon2, enc_lat2, consts)
        decrypted = enc_result.decrypt()[0]

        def plain_haversine(lon1, lat1, lon2, lat2):
            lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            # print("PLAIN: lon1, lat1, lon2, lat2, dlon, dlat: ", lon1, lat1, lon2, lat2, dlon, dlat )
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            # print("plain sin dlat, sin sqrt dlat, sin dlon, sin sqrt dlon: ", math.sin(dlat/2), math.sin(dlat/2)**2, math.sin(dlon/2), math.sin(dlon/2)**2)
            # print("plain cos lat1, cos lat2: ", math.cos(lat1), math.cos(lat2))
            # print("plain a, sqrt a, asin a ", a, math.sqrt(a), math.asin(math.sqrt(a)))
            c = 2 * math.asin(math.sqrt(a))
            # print("plain c ", c)
            return 6371 * c

        expected = plain_haversine(*place1, *place2)

        self.assertAlmostEqual(decrypted, expected, delta=0.5)


if __name__ == '__main__':
    unittest.main()
