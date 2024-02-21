E=0.001
D=0.001
I=1000

while (( $(bc <<< "$E <= 1000") ))
do
    i=0
    while (( i < 100 ))
    do
        python3 ../dp-sgd_new.py --epsilon $E --delta $D --iter $I
        (( i = i + 1 ))
    done
    E=$(bc <<< "$E * 10")
done
