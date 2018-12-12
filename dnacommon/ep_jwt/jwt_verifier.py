from jwt.exceptions import ExpiredSignatureError
import jwt


class EpJwtVerifier:
    def __init__(self, public_key):
        self.public_key = public_key

    def decode(self, token, verify=True):
        jwt_data = EpJwtData(invalid=not verify, expired=not verify)
        try:
            decoded = jwt.decode(token, self.public_key, algorithms=['RS256'], audience="Reporting", verify=verify)
            self.fill_jwt_data(jwt_data, decoded)
        except ExpiredSignatureError as err:
            jwt_data.expired = True
            jwt_data.invalid = True
            print('JWT expired')
        except Exception as err:
            print('Fehler in der JWT Decodierung {0} {1}'.format(err, err.args))
            jwt_data.invalid = True
        return jwt_data

    def fill_jwt_data(self, jwt_data, decoded):
        jwt_data.sub = decoded['sub']
        if 'authorities' in decoded:
            jwt_data.authorities = decoded['authorities']
        if 'partnerid' in decoded:
            jwt_data.partnerid = decoded['partnerid']
        if 'iss' in decoded:
            jwt_data.iss = decoded['iss']
        return jwt_data


class EpJwtData:

    def __init__(self,
                 invalid=False,
                 expired=False,
                 sub=None,
                 iss=None,
                 partnerid=None,
                 authorities=None):
        self.invalid = invalid
        self.expired = expired
        self.sub = sub
        self.authorities = authorities
        self.partnerid = partnerid
        self.iss = iss

    def __str__(self):
        string = "invalid : {invalid} , expired : {expired} , sub : {sub} , authorities : {authorities} , iss : {iss} , partnerid : {partnerid} ".format(
            invalid=self.invalid, expired=self.expired, sub=self.sub, authorities=self.authorities, iss=self.iss,
            partnerid=self.partnerid)
        return string
