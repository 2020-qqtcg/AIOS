# Initialize and update all submodules recursively with a shallow clone of depth 1
git submodule update --init --recursive --depth 1

# Get the absolute path of the current script
SCRIPT_PATH=$(readlink -f "$0")

# Get the directory containing the current script
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

# Change directory to the 'autogen' submodule
cd "$SCRIPT_DIR/autogen"

# Initialize sparse checkout to use the cone mode (simplified sparse-checkout)
git sparse-checkout init --cone

# Set the sparse-checkout to include only the 'autogen' directory
git sparse-checkout set autogen

# Fetch the 'autogen-aios' branch from the remote repository and update the remote reference
git fetch origin autogen-aios:refs/remotes/origin/autogen-aios

# Create a new local branch 'autogen-aios' and set it to track the remote 'autogen-aios' branch
git checkout -b autogen-aios origin/autogen-aios