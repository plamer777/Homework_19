"""This unit provides constants for different purposes like encoding/decoding
password and token, checking required keys, etc."""

# constants for encoding/decoding
HASH_SALT = b'superPlamersecret'
HASH_ITERATIONS = 100000
HASH_ALGO = 'sha256'
JWT_ALGO = 'HS256'
SECRET = '249y823r9v8238r9u'

# the set of required keys
REQUIRED_KEYS = {'username', 'password', 'role'}

# token lifetime
ACCESS_TIME = 30
REFRESH_TIME = 130
