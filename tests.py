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

        place1 = (21.0122, 52.2297)       
        place2 = (21.2122, 52.2197)

        (enc_lon1, enc_lat1), (enc_lon2, enc_lat2) = encrypt_places(place1, place2, context)

        enc_result = enc_haversine(enc_lon1, enc_lat1, enc_lon2, enc_lat2, consts)
        decrypted = enc_result.decrypt()[0]

        expected = haversine(place1[::-1], place2[::-1], unit=Unit.KILOMETERS)

        self.assertAlmostEqual(decrypted, expected, delta=0.5)


if __name__ == '__main__':
    unittest.main()
