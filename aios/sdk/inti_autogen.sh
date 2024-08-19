# Initialize and update all submodules recursively to the commit specified in the parent repository
git submodule update --init --recursive

# Get the absolute path of the current script
SCRIPT_PATH=$(readlink -f "$0")

# Get the directory containing the current script
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

# Change directory to the 'autogen' submodule
cd "$SCRIPT_DIR/autogen"

# Initialize sparse-checkout in "cone" mode for the current repository
# Cone mode simplifies the sparse-checkout configuration
git sparse-checkout init --cone

# Set sparse-checkout to include only the 'autogen' directory
# This means only the specified directory will be checked out, reducing the working directory size
git sparse-checkout set autogen