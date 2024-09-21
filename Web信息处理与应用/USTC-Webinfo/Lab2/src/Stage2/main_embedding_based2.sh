for embed_dim in 16 24 32 48 64
do
    for relation_dim in  16 24 32 48 64
    do
    	python main_Embedding_based.py --seed 2022 \
                               		   --use_pretrain 0 \
                                       --pretrain_model_path 'trained_model/Douban/Embedding_based.pth' \
                               		   --cf_batch_size 1024 \
                              		   --kg_batch_size 2048 \
                              		   --test_batch_size 2048 \
                              		   --embed_dim $embed_dim \
                               		   --relation_dim $relation_dim \
                            		   --KG_embedding_type "TransE" \
                   					   --kg_l2loss_lambda 1e-4 \
                    				   --cf_l2loss_lambda 1e-4 \
                              		   --lr 1e-3 \
                              		   --n_epoch 1000 \
                             		   --stopping_steps 10
    done
done