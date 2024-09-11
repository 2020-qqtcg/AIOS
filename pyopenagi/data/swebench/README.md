# How to run SWE-Bench

## Step 1
In the root directory, run the following code. You can modify config
in `pyopenagi.data.swebench.prepare_text_dataset.CONFIG`.
```shell
python -m pyopenagi.data.swebench.prepare_text_dataset
```
After prepare finished, you will obtain a text dataset under the `output_dir` you
specified. Which has a format like
```text
Dataset({
    features: ['instance_id', 'text', 'repo', 'base_commit', 'problem_statement', 'hints_text', 'created_at', 'patch', 'test_patch', 'version', 'FAIL_TO_PASS', 'PASS_TO_PASS', 'environment_setup_commit'],
    num_rows: 2294
})
```

## Step 2
You need to use text dateset as input for your agent. In fact, `instance_id`
and `text` are enough.
Your agent's output needs to be in the following format.
```text
{
    "instance_id": "<Unique task instance ID>",
    "model_patch": "<.patch file content string>",
    "model_name_or_path": "<Model name here (i.e. SWE-Llama-13b)>",
}
```
Collect all agent output as a `.jsonl` file. Like `predictions.jsonl`.

## Step 3

[//]: # (The evaluation section will be integrated into this directory later.)
Run evaluation following the
[SWE-bench guide](https://github.com/princeton-nlp/SWE-bench/blob/main/assets/evaluation.md).
`--predictions_path` is the path of your `predictions.jsonl`
