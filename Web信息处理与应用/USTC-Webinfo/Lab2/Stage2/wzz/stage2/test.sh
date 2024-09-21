for embed_dim in 16 24 32 48 64
do
    for relation_dim in  16 24 32 48 64
    do
    	python3 ./main_Embedding_based.py --embed_dim $embed_dim --relation_dim $relation_dim
    done
done

for lr in 1e-2 1e-4 5e-4 2e-3
do
    for l2 in 1e-4 1e-5 1e-3 5e-5 2e-4
    do
        if [ "$lr" = "0.01" ]; then
            $l2=1e-3
        fi
    	python3 ./main_Embedding_based.py --lr $lr --kg_l2loss_lambda $l2 --cf_l2loss_lambda $l2 --cuda
    done
done