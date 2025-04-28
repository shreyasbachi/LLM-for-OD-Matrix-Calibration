from vllm import LLM, SamplingParams
llm = LLM(model="meta-llama/Llama-3.3-70B-Instruct", tensor_parallel_size=1, dtype="float16")
params = SamplingParams(temperature=0.7, max_tokens=10)
out = next(llm.generate(prompt="Hello vLLM!", sampling_params=params))
print(out.outputs[0].text)
