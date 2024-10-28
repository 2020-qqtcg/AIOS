## run inference
```shell
python -m experiment.humaneval.inference \
  --data_name gaia-benchmark/GAIA \
  --split test \
  --output_file experiment/gaia_prediction.json \
  --on_aios \
#  --max_num 1 \
  --agent_type autogen \
  --llm_name gpt-4o-mini \
  --max_new_tokens 8000
```
