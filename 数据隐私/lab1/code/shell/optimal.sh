I=0

while (( $(bc <<< "$I < 50") ))
do
    python3 ../elgamal_process.py
    ((I = I + 1))
done