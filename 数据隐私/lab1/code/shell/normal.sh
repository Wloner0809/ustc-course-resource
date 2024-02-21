I=0

while (( $(bc <<< "$I < 200") ))
do
    python3 ../elgamal.py
    ((I = I + 1))
done
