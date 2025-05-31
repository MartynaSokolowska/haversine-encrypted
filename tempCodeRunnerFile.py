def test_enc_haversine(self):
        context = create_ckks_context()

        place1 = (21.0122, 52.2297)       
        place2 = (21.2122, 52.2197)
        (enc_lon1, enc_lat1), (enc_lon2, enc_lat2) = encrypt_places(place1, place2, context)

        enc_result = haversine(enc_lon1, enc_lat1, enc_lon2, enc_lat2, consts)
        decrypted = enc_result.decrypt()[0]

        def plain_haversine(lon1, lat1, lon2, lat2):
            lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            print("PLAIN: lon1, lat1, lon2, lat2, dlon, dlat: ", lon1, lat1, lon2, lat2, dlon, dlat )
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            print("plain sin dlat, sin sqrt dlat, sin dlon, sin sqrt dlon: ", math.sin(dlat/2), math.sin(dlat/2)**2, math.sin(dlon/2), math.sin(dlon/2)**2)
            print("plain cos lat1, cos lat2: ", math.cos(lat1), math.cos(lat2))
            print("plain a, sqrt a, asin a ", a, math.sqrt(a), math.asin(math.sqrt(a)))
            c = 2 * math.asin(math.sqrt(a))
            print("plain c ", c)
            return 6371 * c

        expected = plain_haversine(*place1, *place2)

        self.assertAlmostEqual(decrypted, expected, delta=1.0)