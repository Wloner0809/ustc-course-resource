for lr in 1e-2 1e-4 1e-3
do
    for l2 in 1e-4 1e-5 1e-3 5e-5 2e-4
    do
        python main_Embedding_based.py --seed 2022 \
                                       --use_pretrain 0 \
                                       --pretrain_model_path 'trained_model/Douban/Embedding_based.pth' \
                                       --cf_batch_size 1024 \
                                       --kg_batch_size 2048 \
                                       --test_batch_size 2048 \
                                       --embed_dim 32 \
                                       --relation_dim 32 \
                                       --KG_embedding_type "TransE" \
                                       --kg_l2loss_lambda $l2 \
                                       --cf_l2loss_lambda $l2 \
                                       --lr $lr \
                                       --n_epoch 1000 \
                                       --stopping_steps 10
    done
done