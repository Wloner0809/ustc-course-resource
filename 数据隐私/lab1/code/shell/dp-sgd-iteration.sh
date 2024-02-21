E=100
D=1
I=1

while (( $(bc <<< "$I <= 1000") ))
do
    i=0
    while (( i < 100 ))
    do
        python3 ../dp-sgd.py --epsilon $E --delta $D --iter $I
        (( i = i + 1 ))
    done
    I=$(bc <<< "$I * 10")
done

I=2000

while (( $(bc <<< "$I <= 10000") ))
do
    i=0
    while (( i < 100 ))
    do
        python3 dp-sgd.py --epsilon $E --delta $D --iter $I
        (( i = i + 1 ))
    done
    I=$(bc <<< "$I + 1000")
done
