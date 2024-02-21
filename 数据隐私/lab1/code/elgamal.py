import random
import time
import sympy
import argparse


def is_primitive_root(g, p, factors):
    # determine whether g is a primitive root of p
    for factor in factors:
        if pow(g, (p-1)//factor, p) == 1:
            return False
    return True

def generate_p_and_g(n_bit):
    while True:
        # generate an n-bit random prime number p
        p = sympy.randprime(2**(n_bit-1), 2**n_bit)

        # compute the prime factorization of p-1
        factors = sympy.factorint(p-1).keys()

        # choose a possible primitive root g
        for g in range(2, p):
            if is_primitive_root(g, p, factors):
                return p, g
            

def mod_exp(base, exponent, modulus):
    """TODO: calculate (base^exponent) mod modulus. 
        Recommend to use the fast power algorithm.
    """
    result = 1
    base = base % modulus
    while exponent > 0:
        # 如果指数是奇数，将底数与结果相乘
        if exponent % 2 == 1:
            result = (result * base) % modulus
        # 底数进行平方并取模
        base = (base * base) % modulus  
        # 将指数整除2
        exponent //= 2  
    return result


def elgamal_key_generation(key_size):
    """Generate the keys based on the key_size.
    """
    # generate a large prime number p and a primitive root g
    p, g = generate_p_and_g(key_size)

    # TODO: generate x and y here.
    # x是大于0小于p-1的随机数
    x = random.randint(1, p - 1)
    # 根据ppt的公式: y = g^x mod p
    y = mod_exp(g, x, p)

    return (p, g, y), x

def elgamal_encrypt(public_key, plaintext):
    """TODO: encrypt the plaintext with the public key.
    """
    p, g, y = public_key
    # 随机生成临时密钥k
    k = random.randint(1, p - 1)  
    # 计算临时公钥c1
    c1 = mod_exp(g, k, p)
    # 计算临时密文c2
    c2 = (plaintext * mod_exp(y, k, p)) % p  
    return c1, c2

def elgamal_decrypt(public_key, private_key, ciphertext):
    """TODO: decrypt the ciphertext with the public key and the private key.
    """
    p, g, y = public_key
    x = private_key
    c1, c2 = ciphertext
    # 计算c1的模反演
    s = mod_exp(c1, x, p)
    # 计算s的模逆元
    s_inverse = sympy.mod_inverse(s, p)
    # 计算明文消息
    m = (c2 * s_inverse) % p
    return m

# def check_MultiplicativeHomomorphism(c1, c2, public_key, private_key, m1, m2):
#     # 验证乘法同态性
#     c11, c12 = c1
#     c21, c22 = c2
#     ciphertext1= c11 * c21
#     ciphertext2 = c12 * c22
#     m = elgamal_decrypt(public_key, private_key, (ciphertext1, ciphertext2))
#     if m == m1 * m2:
#         return True
#     else:  
#         return False


if __name__ == "__main__":    
    
    # Version1(测试三个阶段时间版本的代码)
    # # 命令行传参
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--keysize', type=int, default=256)
    # parser.add_argument('--plaintext', type=int, default=100)
    # args = parser.parse_args()
    # key_size = args.keysize
    # plaintext = args.plaintext
    
    # # 密钥生成阶段
    # start1 = time.perf_counter()
    # # generate keys
    # public_key, private_key = elgamal_key_generation(key_size)
    # end1 = time.perf_counter()
    
    # # 加密阶段
    # start2 = time.perf_counter()
    # # encrypt plaintext
    # ciphertext = elgamal_encrypt(public_key, plaintext)
    # end2 = time.perf_counter()

    # # 解密阶段
    # start3 = time.perf_counter()
    # # decrypt ciphertext
    # decrypted_text = elgamal_decrypt(public_key, private_key, ciphertext)
    # end3 = time.perf_counter()
    # print(end1-start1, end2-start2, end3-start3)
    



    
    # Version2(检查乘法同态性)
    # key_size = int(input("Please input the key size: "))

    # # generate keys
    # public_key, private_key = elgamal_key_generation(key_size)
    # print("Public Key:", public_key)
    # print("Private Key:", private_key)
    
    # # 选择是否检查乘法同态性
    # check = input("Do you want to check the Multiplicative Homomorphism? (y/n)")
    # if check == 'y':
    #     plaintext1 = int(input("Please input an integer: "))
    #     plaintext2 = int(input("Please input an integer: "))
    #     ciphertext1 = elgamal_encrypt(public_key, plaintext1)
    #     ciphertext2 = elgamal_encrypt(public_key, plaintext2)
    #     print("Ciphertext1:", ciphertext1)
    #     print("Ciphertext2:", ciphertext2)
    #     m1 = elgamal_decrypt(public_key, private_key, ciphertext1)
    #     m2 = elgamal_decrypt(public_key, private_key, ciphertext2)
    #     print("Decrypted Text1:", m1)
    #     print("Decrypted Text2:", m2)
    #     print("Multiplicative Homomorphism:", check_MultiplicativeHomomorphism(ciphertext1, ciphertext2, public_key, private_key, m1, m2))
    # else :
    #     # encrypt plaintext
    #     plaintext = int(input("Please input an integer: "))
    #     ciphertext = elgamal_encrypt(public_key, plaintext)
    #     print("Ciphertext:", ciphertext)

    #     # decrypt ciphertext
    #     decrypted_text = elgamal_decrypt(public_key, private_key, ciphertext)
    #     print("Decrypted Text:", decrypted_text)





    # Version3(对比乘法同态性质运算的时间开销)
    # key_size = 128

    # # generate keys
    # public_key, private_key = elgamal_key_generation(key_size)
    
    # plaintext1 = 100
    # plaintext2 = 50
    # for i in range(500):
    #     ciphertext1 = elgamal_encrypt(public_key, plaintext1)
    #     ciphertext2 = elgamal_encrypt(public_key, plaintext2)
    #     # 测试先相乘后解密的时间开销
    #     start1 = time.perf_counter()
    #     c11, c12 = ciphertext1
    #     c21, c22 = ciphertext2
    #     ciphertext = c11 * c21, c12 * c22
    #     decrypted_text = elgamal_decrypt(public_key, private_key, ciphertext)
    #     end1 = time.perf_counter()
        
    #     # 测试先解密后相乘的时间开销
    #     start2 = time.perf_counter()
    #     m1 = elgamal_decrypt(public_key, private_key, ciphertext1)
    #     m2 = elgamal_decrypt(public_key, private_key, ciphertext2)
    #     result = m1 * m2
    #     end2 = time.perf_counter()
    #     print(end1-start1, end2-start2)
    
    # # 测试解密函数每条语句的时间开销
    # key_size = 128

    # # generate keys
    # public_key, private_key = elgamal_key_generation(key_size)
    
    # plaintext1 = 100
    # plaintext2 = 5000
    # for i in range(500):
    #     ciphertext = elgamal_encrypt(public_key, plaintext2)
    #     decrypted_text, time1, time2, time3 = elgamal_decrypt(public_key, private_key, ciphertext)
    #     print(time1, time2, time3)
    
    
    


    # Version4(与优化后的结果对比)
    key_size = 128
    public_key, private_key = elgamal_key_generation(key_size)
    start = time.perf_counter()
    for plaintext in range(10000):
        ciphertext = elgamal_encrypt(public_key, plaintext)
        decrypted_text = elgamal_decrypt(public_key, private_key, ciphertext)
    end = time.perf_counter()
    print(end-start)