import os

from pyopenagi.utils.imports import is_swebench_available

if is_swebench_available():
    from swebench.inference.make_datasets.create_text_dataset import main

# Inspired by `swebench.inference.make_datasets.create_text_dataset`
# for detailed meanings of the parameters, please refer to `swebench.inference.make_datasets.create_text_dataset`.
CONFIG = {
    "dataset_name_or_path": "princeton-nlp/SWE-bench",
    "splits": "test",
    "validation_ratio": 0.01,
    "output_dir": "dataset/",
    "retrieval_file": None,
    "prompt_style": "style-3",
    "file_source": "oracle",
    "k": None,
    "max_context_len": None,
    "tokenizer_name": None,
    "push_to_hub_user": None,
}


def create_text_dataset():
    """Create agent input with prompt swe-bench supplied
    """
    if os.environ.get("GITHUB_TOKEN", None) is None:
        raise KeyError("GITHUB_TOKEN environment variable is not set. Swe-bench uses it to clone repositories.")
    main(**CONFIG)


if __name__ == "__main__":
    create_text_dataset()
