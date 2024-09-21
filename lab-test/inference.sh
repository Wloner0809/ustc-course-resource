CUDA_VISIBLE_DEVICES=0 python inference.py \
    --tokenizer_path /data/terencewang/qwen \
    --finetuned_model ./model_140000data_per64batch256_pad/checkpoint-547 \
    --test_data_path ./data/cd/test_5000.json \
    --result_json_data "result_sota.json" \
    --batch_size 1