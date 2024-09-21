python main.py \
    --dataset cd \
    --train_dir baseline \
    --batch_size 128 \
    --lr 0.001 \
    --maxlen 200 \
    --hidden_units 50 \
    --num_blocks 2 \
    --num_epochs 100 \
    --num_heads 1 \
    --dropout_rate 0.2 \
    --l2_emb 0.0 \
    --device cuda \
    # --inference_only true \
    # --state_dict_path cd_baseline/SASRec.epoch=100.lr=0.001.layer=2.head=1.hidden=50.maxlen=200.pth
