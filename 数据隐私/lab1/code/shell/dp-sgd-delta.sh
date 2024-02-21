E=1000
D=0.001
I=1000

while (( $(bc <<< "$D <= 1000") ))
do
    i=0
    while (( i < 100 ))
    do
        python3 ../dp-sgd.py --epsilon $E --delta $D --iter $I
        (( i = i + 1 ))
    done
    D=$(bc <<< "$D * 10")
done
