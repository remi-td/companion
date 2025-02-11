# Companion: A Private and Truthful AI Assistant

Companion is an AI-powered private assistant designed to run locally on your own hardware. It features a classical chat interface but ensures full user control over data and model execution.

## A Minimal, Transparent, and Empowering Implementation

This project is designed to be a **minimal yet powerful implementation**, ensuring full **transparency** in how it operates and empowering users to **understand, modify, and extend** it as needed. By keeping the design simple and modular, Companion enables users to take full control of their AI assistant without hidden dependencies or unnecessary complexity.

## Features

- **Runs Locally**: No external API calls; fully self-contained.
- **Supports Llama-based Models**: Uses `llama cpp` for inference.
- **Persistent Chat Memory**: Persists chats in a database backend built in `sqlite`.
- **Efficient Token Management**: Automatically trims history to fit within the model's context window. Removes thinking traces from chat history.
- **Interactive UI**: Simple and easy-to-use interface built in `Streamlit`.

## Installation

### 1. Prerequisites

- Python 3.10 or later (recommended to use `pyenv`)
- `pip` (latest version)
- **Apple Silicon Users**: Ensure you have an ARM64 Python version.

### 2. Clone the Repository
```bash
git clone https://github.com/remi-td/companion.git
cd companion
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 4. Install Dependencies
This software depends on [llama-cpp](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#build) and its [python bindings](https://github.com/abetlen/llama-cpp-python).
It is crucial for performance that you compile it to exploit your hardware acceleration backend. 
This can be done by setting the CMAKE_ARGS environment variable or via the --config-settings / -C cli flag during installation.
See the [llama.cpp README](https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md) for the list of supported backends and options.

Example:
```bash
export CMAKE_ARGS="-DGGML_METAL=on"  # For macOS Metal acceleration
pip install -r requirements.txt
pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python
```

## Usage

### Obtain a LLM
Get the GGUF file for a llama-cpp-compatible LLM. Eg. [trending on HuggingFace](https://huggingface.co/models?library=gguf&sort=trending).

Tested with:
- [DeepSeek-R1-Distill-Qwen-7B-Q8_0.gguf](https://huggingface.co/bartowski/DeepSeek-R1-Distill-Qwen-7B-GGUF) (recommended)
- [Mixtral_7Bx4_MOE_DPO.i1-IQ4_XS.gguf](https://huggingface.co/mradermacher/Mixtral_7Bx4_MOE_DPO-i1-GGUF)

Update the configuration (see below) to set your model path.
The default location for the model files is the models directory.

### Running the Application
```bash
streamlit run companion/interface.py
```
This will launch the web interface in your browser.

### Chat Interface
- Start a conversation and the assistant will retain context.
- Adjust model parameters like temperature and token limits in the settings.
- Supports streaming responses for real-time interaction.

## Configuration

The model properties are maintained in the file config.yaml under `llm-chat`, and can be adjusted:
- `path`: Path to the LLM's .gguf file
- `temperature`: Controls randomness (0 = deterministic, 1 = high variance)
- `max_tokens`: Maximum output length per response
- `top_p`: Nucleus sampling for diversity
- `n_ctx`: Context window size (trims history automatically)
- `thinking_tag` *(optional, default: `None`)*: Defines the start and end tags for capturing the model's internal reasoning (e.g., `["<think>", "</think>"]`). If set to `None`, thinking traces will not be extracted. extracted thinking traces are displayed but not carried in the model's chat history, and preserved separate from messages in the database bakend.

### Directory Structure
```
companion/
│── companion/
│   ├── __init__.py           # Package initialization
│   ├── interface.py          # Streamlit-based UI
│   ├── llm.py                # Core LLM logic (context management, inference)
│   ├── vector_db.py          # Vector database for embeddings (future)
│   ├── database.py           # Handles persistent storage and context
│   ├── news_browsing.py      # Tool for browsing and summarizing news
│   ├── utils/
│   │   ├── helpers.py        # Helper functions
│── models/                   # Place your GGUF models here
│── requirements.txt          # Dependencies
│── README.md                 # This file
```

## Future Plans

- Integrate SQLite-Vec for retrieval-augmented generation (RAG)
- Expand tooling (e.g., calculator, web search integration)
- Improve UI with more customizations

## Contributing

If you would like to contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit changes (`git commit -m "Added XYZ feature"`)
4. Push to your branch (`git push origin feature-xyz`)
5. Submit a pull request

## License

This project is open-source under the MIT License.

