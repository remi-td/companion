# llm.py
"""
LLM class to handle interactions with large language models (LLMs),
leveraging the llama-cpp-python library for model inference.
Includes tunable parameters like temperature, max tokens, and more.
"""

from llama_cpp import Llama
from config import config 

class LLM:
    def __init__(self):
        """
        Initialize the LLM model using configuration settings from the config.yaml file.
        """
        model_config = config.get("model")
        self.model = Llama(
            model_path=model_config["path"],
            n_gpu_layers=int(model_config.get("n_gpu_layers", 0))
        )

        # Store parameters from the config file
        self.temperature = float(model_config.get("temperature", 0.7))
        self.max_tokens = int(model_config.get("max_tokens", 256))
        self.top_p = float(model_config.get("top_p", 0.9))
        self.n_ctx = int(model_config.get("n_ctx", 2048))

        # Initialize chat context storage
        self.conversation_history = []
        self.conversation_history_tokens = []

    def generate_response(self, prompt, context=None, stream=True):
        """
        Generate a response based on the input prompt, optional context, and conversation history.

        Args:
            prompt (str): The user input or query.
            context (str, optional): Additional context to guide the response generation.

        Returns:
            str: The generated response from the LLM model.
        """
        # Add the user prompt to the conversation history
        self._update_conversation_history(prompt, role="user")

        # Prepare the full context including previous conversation history
        conversation = self._prepare_prompt_with_context(context)

        # Stream the response parts as they are generated
        full_response = ""
        if stream:
            # Call the LLM model to generate a response using the defined parameters
            response_stream = self.model.create_chat_completion(
                messages=conversation,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                stream=True  # Enable streaming
            )

            for chunk in response_stream:
                if 'choices' in chunk and len(chunk['choices']) > 0:
                    delta_content = chunk['choices'][0]['delta'].get('content', '')
                    full_response += delta_content
                    yield delta_content  # Yield each part of the response
        else:
                    # Call the LLM model to generate a response using the defined parameters
            full_response = self.model.create_chat_completion(
                messages=conversation,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                stream=stream
            )

            # Extract and store the response text
            response_text = full_response['choices'][0]['message']['content']

        # Update the conversation history with the assistant's response
        self._update_conversation_history(full_response, role="assistant")
        print("CONVERSATION HISTORY:",self.conversation_history)
    
    def _prepare_prompt_with_context(self, context):
        """
        Combine the conversation history with additional context, such as external data.

        Args:
            context (str, optional): Additional context for the LLM.

        Returns:
            list: A structured list of messages including conversation history and context.
        """
        # Initialize the conversation with system instructions if needed
        conversation = [{"role": "system", "content": "You are an AI assistant."}]

        # Add the conversation history
        conversation.extend(self.conversation_history)

        # Optionally append any external context
        if context:
            conversation.append({"role": "system", "content": context})

        return conversation

    def _update_conversation_history(self, content, role):
        """
        Update the conversation history with the latest message, maintaining structured JSON format.

        Args:
            content (str): The message content (user prompt or model response).
            role (str): The role of the speaker ('user' or 'assistant').
        """
        # Append the new message in the structured JSON format
        self.conversation_history.append({"role": role, "content": content})
        self.conversation_history_tokens.append(len(self.model.tokenize(f"{role}: {content}".encode('utf-8'))))

        # Keep the conversation history manageable (limit history length if needed)
        total_tokens = 0
        i = len(self.conversation_history_tokens) - 1
        # Iterate backward over the token history, expanding the window
        while i >= 0:
            total_tokens += self.conversation_history_tokens[i]
            if (total_tokens >= self.n_ctx - self.max_tokens) or (i==0):
                break
            else:
                i -= 1

        self.conversation_history = self.conversation_history[i:]

    def update_model(self, new_model_path):
        """
        Update the model to a new version or load a different model.

        Args:
            new_model_path (str): Path to the new model file.
        """
        # Load a new model from the given path using llama-cpp-python
        self.model = Llama(model_path=new_model_path)