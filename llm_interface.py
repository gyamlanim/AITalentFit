import os
from openai import AzureOpenAI

class CustomLLM:
    def __init__(self):
        # Azure OpenAI configuration - set these via environment variables
        # (see .env.example) or Streamlit secrets, never hardcode credentials here.
        self.endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.subscription_key = os.environ.get("AZURE_OPENAI_API_KEY")
        self.api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

        if not self.endpoint or not self.subscription_key:
            raise RuntimeError(
                "Missing Azure OpenAI credentials. Set AZURE_OPENAI_ENDPOINT and "
                "AZURE_OPENAI_API_KEY (see .env.example)."
            )

        # Model deployments
        self.chat_deployment = "gpt-4o"
        self.embedding_deployment = "text-embedding-ada-002"  # You may need to update this
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.subscription_key,
        )
    
    def get_embedding(self, content):
        """Generate embedding for the given content"""
        try:
            response = self.client.embeddings.create(
                input=content,
                model=self.embedding_deployment
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            # Return a dummy embedding for testing (1536 dimensions)
            return [0.0] * 1536

    def get_chat_completion(self, prompt, agent_name="assistant"):
        """Get chat completion from the model"""
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a helpful {agent_name} assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4096,
                temperature=0.7,
                top_p=1.0,
                model=self.chat_deployment
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in get_chat_completion: {e}")
            return f"Error: Could not get completion - {str(e)}"


