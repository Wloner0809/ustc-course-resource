import random
import sympy
from concurrent.futures import ProcessPoolExecutor
import time

def is_primitive_root(g, p, factors):
    for factor in factors:
        if pow(g, (p - 1) // factor, p) == 1:
            return False
    return True

def generate_p_and_g(n_bit):
    while True:
        p = sympy.randprime(2 ** (n_bit - 1), 2 ** n_bit)
        factors = sympy.factorint(p - 1).keys()
        for g in range(2, p):
            if is_primitive_root(g, p, factors):
                return p, g

def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def elgamal_key_generation(key_size):
    p, g = generate_p_and_g(key_size)
    x = random.randint(1, p - 1)
    y = mod_exp(g, x, p)
    return (p, g, y), x

def elgamal_encrypt(public_key, plaintext):
    p, g, y = public_key
    k = random.randint(1, p - 1)
    c1 = mod_exp(g, k, p)
    c2 = (plaintext * mod_exp(y, k, p)) % p
    return c1, c2

def elgamal_decrypt(public_key, private_key, ciphertext):
    p, _, _ = public_key
    x = private_key
    c1, c2 = ciphertext
    s = mod_exp(c1, x, p)
    s_inv = sympy.mod_inverse(s, p)
    plaintext = (c2 * s_inv) % p
    return plaintext

def encrypt_wrapper(args):
    public_key, plaintext = args
    return elgamal_encrypt(public_key, plaintext)

def decrypt_wrapper(args):
    public_key, private_key, ciphertext = args
    return elgamal_decrypt(public_key, private_key, ciphertext)

def parallel_encrypt(public_key, plaintext_batch):
    args_list = [(public_key, plaintext) for plaintext in plaintext_batch]
    with ProcessPoolExecutor() as executor:
        encrypted_batch = list(executor.map(encrypt_wrapper, args_list))
    return encrypted_batch

def parallel_decrypt(public_key, private_key, ciphertext_batch):
    args_list = [(public_key, private_key, ciphertext) for ciphertext in ciphertext_batch]
    with ProcessPoolExecutor() as executor:
        decrypted_batch = list(executor.map(decrypt_wrapper, args_list))
    return decrypted_batch

if __name__ == "__main__":
    key_size = 128
    
    public_key, private_key = elgamal_key_generation(key_size)
    plaintext_batch = [plaintext for plaintext in range(10000)]
    
    start = time.perf_counter()
    encrypted_batch = parallel_encrypt(public_key, plaintext_batch)
    decrypted_batch = parallel_decrypt(public_key, private_key, encrypted_batch)
    end = time.perf_counter()
    
    print(end-start)