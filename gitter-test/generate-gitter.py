from pqcrypto.kem.ml_kem_1024 import generate_keypair

pub, sec = generate_keypair()
with  open("gitter.pub", "wb") as fd:
    fd.write(pub)
#
with  open("gitter.sec", "wb") as fd:
    fd.write(sec)
#

# for RSA det er ikke så lett å lagre nøkløene "rå" rett og slett fordi
# de inneholder flere tall (n, e, og d).  
# Vi bruker det minste formatet, som er DER
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

rsa_priv = rsa.generate_private_key(public_exponent=65537, key_size=15360)
rsa_pub = rsa_priv.public_key()

# Ut med den private, kodet som BER
with open("rsa.priv", "wb") as fd:
    rå_priv = rsa_priv.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    fd.write(rå_priv)
#
# Ut med den offentlige
with open("rsa.pub", "wb") as fd:
    rå_pub = rsa_pub.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    fd.write(rå_pub)
#
