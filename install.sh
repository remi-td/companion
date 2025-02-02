#!/bin/bash
# This is a MacOs implementation using pyenv!

pyenv virtualenv 3.10.4 comp_dev
pyenv activate comp_dev

# Set environment variables for llama-cpp-python build
export CMAKE_ARGS="-DGGML_METAL=on" #now default on macos, so should not be needed, but change as/if needed to support your platform (https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md)
export CPATH=$(xcrun --sdk macosx --show-sdk-path)/usr/include/c++/v1             
export CPLUS_INCLUDE_PATH=$(xcrun --sdk macosx --show-sdk-path)/usr/include/c++/v1

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Force rebuild and reinstall llama-cpp-python from source
#pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python