import random
import sympy
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

def elgamal_encrypt_batch(public_key, plaintext_batch):
    p, g, y = public_key
    k_values = [random.randint(1, p - 1) for _ in range(len(plaintext_batch))]
    c1_values = [mod_exp(g, k, p) for k in k_values]
    c2_values = [(plaintext * mod_exp(y, k, p)) % p for plaintext, k in zip(plaintext_batch, k_values)]
    return list(zip(c1_values, c2_values))

def elgamal_decrypt_batch(public_key, private_key, ciphertext_batch):
    p, _, _ = public_key
    x = private_key
    s_values = [mod_exp(c1, x, p) for c1, _ in ciphertext_batch]
    s_inv_values = [sympy.mod_inverse(s, p) for s in s_values]
    plaintext_values = [(c2 * s_inv) % p for (_, c2), s_inv in zip(ciphertext_batch, s_inv_values)]
    return plaintext_values

if __name__ == "__main__":
    key_size = 128
    
    start = time.perf_counter()
    public_key, private_key = elgamal_key_generation(key_size)
    # 批量加密
    plaintext_batch = [100, 101, 102, 103, 104]
    ciphertext_batch = elgamal_encrypt_batch(public_key, plaintext_batch)
    # 批量解密
    decrypted_batch = elgamal_decrypt_batch(public_key, private_key, ciphertext_batch)     
    end = time.perf_counter()
    
    print(end-start)