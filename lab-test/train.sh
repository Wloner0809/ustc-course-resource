CUDA_VISIBLE_DEVICES=3 python train.py \
    --base_model /data/terencewang/qwen \
    --train_data_path "[\"./data/cd/train.json\"]" \
    --val_data_path "[\"./data/cd/valid_5000.json\"]" \
    --output_dir /data3/terencewang/model_140000data_per64batch256\
    --batch_size 256 \
    --micro_batch_size 64 \
    --num_epochs 1 \
    --learning_rate 1e-4 \
    --cutoff_len 512 \
    --seed 0 \
    --sample 140000 \
    # --train_on_inputs \
    # --group_by_length \
