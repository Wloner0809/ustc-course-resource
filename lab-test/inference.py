import fire
import torch
import json
import os
from transformers import GenerationConfig, AutoTokenizer
from transformers import AutoModelForCausalLM
from tqdm import tqdm


os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
torch.set_num_threads(1)
device = "cuda" if torch.cuda.is_available() else "cpu"
try:
    if torch.backends.mps.is_available():
        device = "mps"
except:  # noqa: E722
    pass


def main(
    tokenizer_path: str = "data/tokenizer.json",
    finetuned_model: str = "",
    test_data_path: str = "data/test.json",
    result_json_data: str = "result.json",
    batch_size: int = 16,
):
    "tokenizer setting"
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    tokenizer.padding_side = "left"
    # tokenizer.pad_token_id = 0
    tokenizer.pad_token_id = 151644

    "model setting"
    if device == "cuda":
        model = AutoModelForCausalLM.from_pretrained(
            finetuned_model,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        model = model.to(device)
    elif device == "mps":
        model = AutoModelForCausalLM.from_pretrained(
            finetuned_model,
            device_map={"": device},
            torch_dtype=torch.bfloat16,
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            finetuned_model, device_map={"": device}, low_cpu_mem_usage=True
        )
    # model.config.pad_token_id = 0
    model.config.pad_token_id = 151644
    model.eval()

    def generate_prompt(instruction, input=None):
        if input:
            return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.  

    ### Instruction:
    {instruction}

    ### Input:
    {input}

    ### Response:
    """
        else:
            return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.  

    ### Instruction:
    {instruction}

    ### Response:
    """

    def evaluate(
        instructions,
        inputs=None,
        temperature=0,
        top_p=0.9,
        top_k=40,
        num_beams=4,
        max_new_tokens=128,
        # max_new_tokens=32,
        **kwargs,
    ):
        prompt = [
            generate_prompt(instruction, input)
            for instruction, input in zip(instructions, inputs)
        ]
        inputs = tokenizer(
            prompt, return_tensors="pt", padding=True, truncation=True
        ).to(device)
        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            num_return_sequences=num_beams,
            # pad_token_id=tokenizer.eos_token_id,
            pad_token_id=151644,
            eos_token_id=tokenizer.eos_token_id,
            **kwargs,
        )
        with torch.no_grad():
            generation_output = model.generate(
                **inputs,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )
        s = generation_output.sequences
        output = tokenizer.batch_decode(s, skip_special_tokens=True)
        output = [_.split("Response:\n")[-1].strip() for _ in output]
        real_outputs = [
            output[i * num_beams : (i + 1) * num_beams]
            for i in range(len(output) // num_beams)
        ]
        return real_outputs

    outputs = []
    with open(test_data_path, "r") as f:
        test_data = json.load(f)
        instructions = [_["instruction"] for _ in test_data]
        inputs = [_["input"] for _ in test_data]

        def batch(list, batch_size=batch_size):
            chunk_size = (len(list) - 1) // batch_size + 1
            for i in range(chunk_size):
                yield list[batch_size * i : batch_size * (i + 1)]

        for i, batch in tqdm(enumerate(zip(batch(instructions), batch(inputs)))):
            instructions, inputs = batch
            output = evaluate(instructions, inputs)
            outputs = outputs + output

        for i, test in tqdm(enumerate(test_data)):
            test_data[i]["predict"] = outputs[i]

    with open(result_json_data, "w") as f:
        json.dump(test_data, f, indent=4)


if __name__ == "__main__":
    fire.Fire(main)
