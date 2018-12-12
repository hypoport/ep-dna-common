from unittest import TestCase

import jwt

from dnacommon.ep_jwt.jwt_verifier import EpJwtVerifier

PUBLIC_KEY_PEM = "-----BEGIN PUBLIC KEY-----\n" \
                 "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5jlMInKX520FDjW/qGo/\n" \
                 "q311nCpwuGrUpFe/1XeOOcb4dExYq2UibJrXNLFNSGX9ul0bZCJcY9lU7DqtYh9u\n" \
                 "b+6o3Z9pf/vLbVUShmUCeyR3akpTu0fUwAkT+EwZW/M70YfZhNdaXuDZqK3tre0W\n" \
                 "HpqWekWHJXhJ7Dvq8urhHjbiP6hC0fzyR4aSK9L1Cd7fAVhdYpiPYm4L09gG47qu\n" \
                 "HPHOVqkicPMqB6tBqoZugqCqT3g+T6IX3bqwdIwVXnlPTgz5MZSOZ6081SM9XjTL\n" \
                 "Q/xiNsurdwrpSmAY7rrqHDsaGo/QPAPrVRsK0+K8HVqc4v++OApqQvwcBMpwiCBT\n" \
                 "gwIDAQAB\n" \
                 "-----END PUBLIC KEY-----"

EP2_PUBLIC_KEY_PROD = "-----BEGIN PUBLIC KEY-----\n" \
                      "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4nbIXnSUhplUd+Xz2kb1\n" \
                      "M8SHbIu0sMJcTfqkTXtDzr+WkbOgmeDGKsRx7g4wYOYfooPU9WS4onveQ4dsBEn6\n" \
                      "nlMq+Q1sPnX5J5lvoF0TDD6cGV6pnTZAEY1Xp7o5IYxCIwl32tdHQI+JgsDscsoe\n" \
                      "O+eAEl/tkRGrAKXOSVTJGZgQ1z4zmgRYj31LuyuXgDKeGhoCJnhZUuMLHAMUnxFo\n" \
                      "Bh4d109wm5+C4gosAzqbD/qXiqx8aOQlszRt2p14usAXsrP4EdypbLllQzxWy5cv\n" \
                      "yCB4yByj9d4BDPgssTRbGd85crlXSB9WCaHBZ23b1aBFfSYljoqE/35m6cR74w3u\n" \
                      "QQIDAQAB\n" \
                      "-----END PUBLIC KEY-----"
EP2_PUBLIC_KEY_MTP = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5jlMInKX520FDjW/qGo/\nq311nCpwuGrUpFe/1XeOOcb4dExYq2UibJrXNLFNSGX9ul0bZCJcY9lU7DqtYh9u\nb+6o3Z9pf/vLbVUShmUCeyR3akpTu0fUwAkT+EwZW/M70YfZhNdaXuDZqK3tre0W\nHpqWekWHJXhJ7Dvq8urhHjbiP6hC0fzyR4aSK9L1Cd7fAVhdYpiPYm4L09gG47qu\nHPHOVqkicPMqB6tBqoZugqCqT3g+T6IX3bqwdIwVXnlPTgz5MZSOZ6081SM9XjTL\nQ/xiNsurdwrpSmAY7rrqHDsaGo/QPAPrVRsK0+K8HVqc4v++OApqQvwcBMpwiCBT\ngwIDAQAB\n-----END PUBLIC KEY-----"

# EP2_PUBLIC_KEY_PROD = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4nbIXnSUhplUd+Xz2kb1\n" \
#                       "M8SHbIu0sMJcTfqkTXtDzr+WkbOgmeDGKsRx7g4wYOYfooPU9WS4onveQ4dsBEn6\n" \
#                       "nlMq+Q1sPnX5J5lvoF0TDD6cGV6pnTZAEY1Xp7o5IYxCIwl32tdHQI+JgsDscsoe\n" \
#                       "O+eAEl/tkRGrAKXOSVTJGZgQ1z4zmgRYj31LuyuXgDKeGhoCJnhZUuMLHAMUnxFo\n" \
#                       "Bh4d109wm5+C4gosAzqbD/qXiqx8aOQlszRt2p14usAXsrP4EdypbLllQzxWy5cv\n" \
#                       "yCB4yByj9d4BDPgssTRbGd85crlXSB9WCaHBZ23b1aBFfSYljoqE/35m6cR74w3u\n" \
#                       "QQIDAQAB"

PRIVATE_KEY_PEM = "-----BEGIN PRIVATE KEY-----\n" \
                  "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDmOUwicpfnbQUO\n" \
                  "Nb+oaj+rfXWcKnC4atSkV7/Vd445xvh0TFirZSJsmtc0sU1IZf26XRtkIlxj2VTs\n" \
                  "Oq1iH25v7qjdn2l/+8ttVRKGZQJ7JHdqSlO7R9TACRP4TBlb8zvRh9mE11pe4Nmo\n" \
                  "re2t7RYempZ6RYcleEnsO+ry6uEeNuI/qELR/PJHhpIr0vUJ3t8BWF1imI9ibgvT\n" \
                  "2Abjuq4c8c5WqSJw8yoHq0Gqhm6CoKpPeD5PohfdurB0jBVeeU9ODPkxlI5nrTzV\n" \
                  "Iz1eNMtD/GI2y6t3CulKYBjuuuocOxoaj9A8A+tVGwrT4rwdWpzi/744CmpC/BwE\n" \
                  "ynCIIFODAgMBAAECggEAXo5n87oHI9kF+4kd16kTz3Zu6J4Rv9y4y2ry8lTxSE+t\n" \
                  "We7FeFfIZLzP6Odta2/gXzvAdUcblTL9Cy0qayOnszddifDgXt1m9te7DRHNjBA1\n" \
                  "L6WpcEEXY2wXFKMEw1xKVEusjj/48QD+xKXy+b1nmVg6t6t4z23xRqJxZCYOId73\n" \
                  "Wg47fAQlX581b84CkkmEfnYE4+lFagB621fJI47ZX4LaXz5ea2WYjdtyQh9TXFde\n" \
                  "PKdfuhR6Qi3xTKI+nkjFPh89CVkMF+f8cWi/iC9UwXoREYV71ht4LJRwk6lhkAn/\n" \
                  "lI9av0CYLbxwhN0dHG7Jgb2Rlz7UofeJRk1Muyrv6QKBgQD5/HEYCH6n7vo4rYYo\n" \
                  "FvvSugl4Ik8lusf3/vHF+fYS5ZflhsGS0vl3YP33B84hbgKk5aSiIy1sbIJrgfz7\n" \
                  "b31uqsks3oKUiRSXizjv2woCz8hjrJNoUFmQZRP0EqxhK7h151qjehKoDAHBb3cg\n" \
                  "kOWKhiEElRMx/bULShqJZv9mXwKBgQDrwyXrSBqAEIvryX87esGU8qEfMOp5P/bC\n" \
                  "G5O0mSe/J179P+8KJVnN22A0wWyq0kN5PoS76oaHESjd7nH3sw2cJu+nwnzL1oyo\n" \
                  "qUly1UPTR2jIebQz3J7RVFa36dG2NN421ynh+BL+Rcrs6qrpQ9p8Lvrm+deULLNG\n" \
                  "qBQlP7y9XQKBgQCUcjCiSeEUThfucjSZN9TANNMMsKr5R6oZfR4LJzzVydriZJws\n" \
                  "WPXkywbkm5DvTwlo7ClQUr1VhjYIKz+T+4eroOUnrNYz6Bb/SqA75oFSXBqt/bvn\n" \
                  "FNeqpCsuI6yTY0f9U64CJ6pOehrMyCkggIqeMLoIo5GrfPH2S0Ho1+3P1wKBgATG\n" \
                  "/420+FSAAVXVz241HpcWE42+QAIU+bsVM/kE4XlOIu6ezQk3mIpDV7+566nKePOM\n" \
                  "AMSODAvQnTNiEY0jY7M2VsTffAflYRRJ2eMpzyYI3GazkKM8ZTt4qgkwA7/dcmNK\n" \
                  "GN8rV7cvUt1aI/x2E4dQrGThyyyFe1yDK2VV1U1BAoGBAOOOnloOGc5MbhRrJzpx\n" \
                  "iz7Hpev3y9CGNIgZATxlkuAVrQotzuOn1BXg9F/EQy/lfEtDeqpr9zcotNO+7+2i\n" \
                  "hxXRGEEUlfvJRhSHhihc+rJD7hvcUwwE2Sko0xz3sxq2Alxm+8Ikq9Z2DVyp/xjV\n" \
                  "QDpI2XRvmmBYhiGOedcQH38Q\n" \
                  "-----END PRIVATE KEY-----"

JWTOKEN_EXPIRED = "eyJpc3MiOm51bGwsImFsZyI6IlJTMjU2In0.eyJleHAiOjE0NjU0OTIwMzYsImlhdCI6MTQ2NTQ5MjAzNn0.5OnFXN_at0YjhIWrewZTHpXv7EUAWtab0-NJEQNLcl80EAq7OVVdTu1jb0N_2OyplUohrUuc9UIHk0IJzAOzGkoFujEfTEs3dnoAsloaH_c2OKQIP3_3NmY09_NyyAFAVFlHVNMIdzN4447HOa7LhvaRxbrt_tmeHTIaKwnoQjgHNu2EfbgGLj_ayK0VlS9kERsFYHlYtv2swTsAaW3ALH07VmpSt9AGPfYzY5egwYiTFXTBTtTaTsLTUsiqCC47GxaSsMzt8B0NzJlCdti3JShlxWHa3pia6CJ1O2bRSHmg_lpvhEPEVNSB0yun9rCFvIrCVoqWzY06mySOMbfUDw"
JWTOKEN_EP2_EXPIRED = "eyJhbGciOiJSUzI1NiIsImlzcyI6IlZHRDQzIn0.eyJleHAiOjE0NjU1Nzg2NTgsInN1YiI6IkZFRjEwIiwic3ViLW9laWQiOiI0ZTRiNzk4OWZiMjYwMDE1YWFlYWI3ODMiLCJiZW51dHplck5hbWUiOiJqZW5zLmhhbmFja0BoeXBvcG9ydC5kZSIsImF1dGhvcml0aWVzIjpbIk5FV19GRUFUVVJFX1ZJU0lCTEUiLCJFQ0hURVNfR0VTQ0hBRUZUX0VSTEFVQlQiLCJFUENfRVhQT1JUX0VSTEFVQlQiLCJERVZfVE9PTFNfQVZBSUxBQkxFIiwiS1JFRElUX1NNQVJUX1NJQ0hUQkFSIiwiREFSRl9FSU5TVEVMTFVOR0VOX09FRkZORU4iXSwibmFtZSI6IkplbnMgSGFuYWNrIiwiaWF0IjoxNDY1NDkyMjU4LCJ2byI6IkhZUE9QT1JUIn0.gsr7JOva7a6tyYL5YA0UBp3KNSFcY8PcUwatqj9HJoDa6o6MavnPH2pvQZ1QURJlku8iJPBfr2JyMnsVS9SNanzQ0sM4S9bJOjOipXR-48KjN1_1u__PhataACq8fgv5Os-KUPDqzZMJJ0CPx5MoXJKMXrQHe47KobBMxTk7GAdpMG1TtYF_-5Ai2AkPB56nbyYjpAOdCUmiLINxIq8W1bc-S1h-DTSYFmb060T7pzcmMSlV7Lno9Zz6zvtUpkCvxpVNmSnZ1ALol5CXDIuJQTBBu_kvqPAgckTLwisX6z0DlEfHsQuWoKf-fUMxdHLu1ooSaaGzazaT9D6dQsnKPQ"
# JWTOKEN_VALID = "eyJhbGciOiJSUzI1NiIsImlzcyI6IlZHRDQzIiwidHlwIjoiSldUIn0.eyJleHAiOjE0ODMwMDI4MTQsInN1YiI6IlNQS19CQVJOSU0iLCJhdXRob3JpdGllcyI6WyJQUk9EVUtUQU5CSUVURVJfUkVQT1JUX0FCUlVGIl0sIm93bmVyIjoiRkVGMTAiLCJpc3MiOiJWR0Q0MyIsImp0aSI6IjlvK2xPRUtjc0RYSURKc0d1K2hMQVZFaWZzRkQ2Q1wvOCIsImlhdCI6MTQ4MzAwMjc1NH0.OcG2sUNifgVLleQdrrZ-Jca4UtadFlWRiKcVb1BaSUIJl9K5qc3UyW3O5NpWgoQ18kYrb_98iBYApqRsKFVWfLW1GLncWj3nKX3-wowCm35uz0u9-vm5kQ-UU0gPCn7CtTZwcasdY2FeTg7UZs6VgLrakZKu8dK1QZJRPW89jo908r4LrEeHUCjdR_9obdoDQ0R97Fs4jp4JbBTRQ6cMkesNhzXybajSphO_YSD9uwac3hhqw0R-tWiwrYcaCtFOUpYigjP-M6OgMAs63mSbmfGe0Hrn5MrrRZdvKd7ovzGM1r3O_k2gRpOBDANSymm831BCC9Ss5tsbmmLCu2gUzg"
# JWTOKEN_VALID = "eyJjdHkiOiJhd3MrcmVwb3J0aW5nIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJWR0Q0MyIsInN1YiI6IldFUjAzIiwicGFydG5lcmlkIjoiV0VSMDMiLCJhdXRob3JpdGllcyI6WyJST0hEQVRFTl9BQlJVRiJdLCJleHAiOjE1Mjc2ODUwOTMsImF1ZCI6IlJlcG9ydGluZyJ9.uOvmDft9Cl5E3NoOQxFRBcY1Btn06eREIY-bk_0_A7ayehzx8WVpCnOvHjI5mH2srGqUKlrEmHvYxU0nF0h4l4BlLl5T2jc-KOBcDtV-ARlASti7vfx1gTEqoLuUo_Kj0eFTPkZIEzByHnzOLreCOnzFg5hl0SzJDwG3bDcjDoFsGa53Ikboeh7zDZtVDQDYcG6_FSfYhUdk2Ig78e8rVxrB9DrQDttk0VZVIULXa_1zdcT31LXs2DHLJAhGHA06xOYvFzTa73lE4S6r9sz4KnikSvpr2IRPWoRsMUlhupSMlsqAd7aPepp_GNKqLVC48rAanoSEoVZQbl0TnDLw7g"
# JWTOKEN_VALID = "eyJjdHkiOiJhd3MrcmVwb3J0aW5nIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJWR0Q0MyIsInN1YiI6IldFUjAzIiwicGFydG5lcmlkIjoiV0VSMDMiLCJhdXRob3JpdGllcyI6WyJST0hEQVRFTl9BQlJVRiJdLCJleHAiOjE1Mjc2ODU0MjYsImF1ZCI6IlJlcG9ydGluZyJ9.gPMZFt61ACOV0E8-kGASi1Pv51TGvxz1MWZvremRv-xcmpL4GVvgnYjS4a99aIItw165dU0bLhXmJHxfrvLltPA2TfD5AitO8BCchYZsY6HeOAtrTp2dAyx06sIZG4-ADam8l43HI3wNB3TX5r_wdsjBr8PsLFd4I6w31JJ7OgFcHjfQ-1aXW0iLi8h6w_paBhpuGkB9-_kYpkk6zYpNDir9Ixv5PmpBCaj0Hmp8Sv7r_XfBd0QEW2hGis6ennFRnJv9tlEm3ngFnu3TQ7I0RN5qDYchU6Ba83OYMOgj4F3kMEXkeJKs6GuPGD2sPU3zS3NoHaxNIMoXKGBkaBzO6g"
JWTOKEN_VALID = "eyJjdHkiOiJhd3MrcmVwb3J0aW5nIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJWR0Q0MyIsInN1YiI6IldFUjAzIiwicGFydG5lcmlkIjoiV0VSMDMiLCJhdXRob3JpdGllcyI6WyJST0hEQVRFTl9BQlJVRiJdLCJleHAiOjE1Mjc3NTI0OTksImF1ZCI6IlJlcG9ydGluZyJ9.bjaZBVgQ_Ci3a8un-RWHgk_rYCoaWOD4nbWJxQqPaVfHkF6rtBeMnwj89uSA6K5xe88igErg01dWUzy1qDY9JuqzXt6mBUEZ4Wxpp-fGRzWoIGRHPFZuIIhLHyZDPIYs4n1JzqXEJ6kaXPOEwNjLtcRCzEdkDRq0a8Ac8lxcl705i6ces5tkUASrUnY_OZszU1hNBjViXWwqDf26Tv-adyU4eJ73U00FhHTZD6UByUXjCXE6kzK4kfjMvuvFNjv_QsrBhr5UfutiGFVPfMhY-gcpK-0nTIe2DCMpSJyeDqDV7YqETKSGFE8urFZKsB9q97is-ftii9gdHFxHOIzshg"

JWTOKEN_PUBKEY_EIGELB = PUBLIC_KEY_PEM
# JWTOKEN_EIGELB = "eyJpc3MiOiJWR0Q0MyIsImFsZyI6IlJTMjU2IiwidHlwIjoiSldUIn0.eyJvd25lciI6IldFUjAzIiwic3ViIjoiTVVTVEVSQkFOSyIsImlzcyI6IlZHRDQzIiwiZXhwIjoxNTEzNzg3OTEwLCJpYXQiOjE1MTM3ODc4NTAsImF1dGhvcml0aWVzIjpbIlBST0RVS1RBTkJJRVRFUl9SRVBPUlRfQUJSVUYiXSwianRpIjoiNTBNXC9GaVwvR3FuSWJ0RjdJRGFMZzBrME1hcTVkZ3BjZyJ9.oooQO6oDq8045G4WNrquicUTVL58h5EmqDNj38v8k7ed0sSVLBoHwKPakR7uNJja130qqJcmyezryq-O-b1IGHdy-mpn6ZlmViDw6LfpB7PsPsTw2R5IgzayThc4Anw4JSxAWb7TUZdqQ0gPXB-kSUAv7SrHm1MdDInKHjHjXAkV7gitHkSiRWD-9tK0uF5qR3Yv-sJyd_UDxWJciiCKsWDdsQPfvmVVWt2i5koRBndmtU5n6BI9zQwin_k6mEws5qc45yRvpMSfxM4l2_0LXoBhuUTRMtWVm9yFguVD0sFeBp6pVB28Oi4qt428WMfW103-fUm7_h0M1rre16dZPA"
JWTOKEN_EIGELB = "eyJpc3MiOiJWR0Q0MyIsImFsZyI6IlJTMjU2IiwidHlwIjoiSldUIn0.eyJvd25lciI6IldFUjAzIiwic3ViIjoiTVVTVEVSQkFOSyIsImlzcyI6IlZHRDQzIiwiZXhwIjoxNTEzODQ3NDAwLCJpYXQiOjE1MTM4NDczNDAsImF1dGhvcml0aWVzIjpbIlBST0RVS1RBTkJJRVRFUl9SRVBPUlRfQUJSVUYiXSwianRpIjoiU2JYTWFiMysrTERtaHA2WWYwZis3dDVaa0FCOUNmeGIifQ.1_4B0lXS9QNser_x_5TxJjIgkmZVCfMt6zeFNYxmgiisWgV9UC_T3NI3kKlPGGYfS0rVsnScMYdATYv4ooNoLUd5sD7aidmlugau33bio4trVfEIOGtsL3VaUQw1vjJl11u-BNxnJJvzI3QDUaH9KrjBrxU97cj65bHE2byoUtqnbv3rRwvUU4eYoicOEO0ZYwBLLeSlkzCmERNw7XsOdCIc6fTClzLI5bVpDmzmCemFBgADqmAKnBxxa6dZrZjg0YhTcn1vaKS1tGML-_MeMkdE4lH_MkuWyZC9KZkNRrXpk4n6s2z2ubDHfAjAuWpXBLZlviGaGORHCiZ82uJS8g"


class JwtVerifierTest(TestCase):
    def setUp(self):
        self.jwt_verifier = EpJwtVerifier(public_key=EP2_PUBLIC_KEY_PROD);

    def test_manuell(self):
        jwt_verifier = EpJwtVerifier(public_key=EP2_PUBLIC_KEY_MTP);
        jwt_daten = jwt_verifier.decode(JWTOKEN_VALID, verify=True)
        print(jwt_daten)
        self.assertTrue(jwt_daten.invalid)

    def test_expired(self):
        jwt_daten = self.jwt_verifier.decode(JWTOKEN_EP2_EXPIRED, verify=True)
        self.assertTrue(jwt_daten.invalid or jwt_daten.expired)

    def test_verification(self):
        data = self.jwt_verifier.decode(JWTOKEN_EXPIRED, verify=True)
        self.assertTrue(data.invalid)

    def test_invalid(self):
        data = self.jwt_verifier.decode('XXXXXX', verify=True)
        self.assertTrue(data.invalid)

    def test_decode(self):
        jwtoken = JWTOKEN_VALID
        public_key = EP2_PUBLIC_KEY_MTP
        # algo = 'HS256' , 'ES256', 'PS256', 'RS256'
        algo = 'RS256'
        with self.assertRaises(Exception) as context:
            self.jwt_verifier.decode(jwtoken, public_key, algorithms=[algo], verify=True)
        self.assertTrue('Signature has expired' in str(context.exception))

    def test_decode(self):
        jwtoken = JWTOKEN_EIGELB
        public_key = PUBLIC_KEY_PEM
        # algo = 'HS256' , 'ES256', 'PS256', 'RS256'
        algo = 'RS256'
        print(jwt.decode(jwtoken, 'x', algorithms=[algo], verify=False))
