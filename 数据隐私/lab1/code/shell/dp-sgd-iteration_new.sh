E=10
D=0.001
I=1

while (( $(bc <<< "$I <= 100") ))
do
    i=0
    while (( i < 100 ))
    do
        python3 ../dp-sgd_new.py --epsilon $E --delta $D --iter $I
        (( i = i + 1 ))
    done
    I=$(bc <<< "$I * 10")
done

I=200

while (( $(bc <<< "$I <= 1000") ))
do
    i=0
    while (( i < 100 ))
    do
        python3 dp-sgd_new.py --epsilon $E --delta $D --iter $I
        (( i = i + 1 ))
    done
    I=$(bc <<< "$I + 100")
done

I=2000

while (( $(bc <<< "$I <= 5000") ))
do
    i=0
    while (( i < 100 ))
    do
        python3 dp-sgd_new.py --epsilon $E --delta $D --iter $I
        (( i = i + 1 ))
    done
    I=$(bc <<< "$I + 1000")
done