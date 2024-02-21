keysize=32
plaintext=100
while (( $keysize <= 192 ))
do
    i=0
    while (( i < 100 ))
    do
        python3 ../elgamal.py --keysize $keysize --plaintext $plaintext
        (( i = i + 1 ))
    done
    (( keysize = keysize + 32 ))
done