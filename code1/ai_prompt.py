import os
import openai
from typing import Dict, Any, List, Optional
import time
import logging

# Check OPENAI_API_KEY
from dotenv import load_dotenv
load_dotenv()   
api_key = os.environ.get('OPENAI_API_KEY')
try:
    # your risky code here
    if api_key:     
        # self.log("OPENAI_API_KEY is set after calling load_dotenv()")
        if not api_key.startswith('sk-proj-') or len(api_key)<12:
            self._log_warning("OPENAI_API_KEY format looks incorrect after calling load_dotenv()")
    else:   
        self._log_warning("OPENAI_API_KEY environment variable is not set after calling load_dotenv()")
except Exception as e:
    print(f"An error occurred: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OpenAIClient:
    """A client for handling OpenAI API interactions safely."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable.
            model: The model to use for generation.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as OPENAI_API_KEY environment variable")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        
    def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        max_retries: int = 3,
        retry_delay: int = 2,
        system_message: str = "You are a helpful assistant."
    ) -> Dict[str, Any]:
        """
        Generate text safely with error handling and retries.
        
        Args:
            prompt: The user prompt for text generation
            max_tokens: Maximum tokens in the response
            temperature: Sampling temperature (0.0-2.0)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            system_message: System message to set context
            
        Returns:
            The API response as a dictionary
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return self._parse_response(response)
                
            except openai.APIError as e:
                logger.error(f"API error: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    logger.error("Max retries reached")
                    raise
                    
            except openai.RateLimitError:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                logger.warning(f"Rate limit hit. Waiting {wait_time} seconds")
                time.sleep(wait_time)
                if attempt == max_retries - 1:
                    raise
                    
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise
    
    def _parse_response(self, response) -> Dict[str, Any]:
        """Extract and validate the response content."""
        try:
            if hasattr(response, 'choices') and len(response.choices) > 0:
                return {
                    "text": response.choices[0].message.content,
                    "finish_reason": response.choices[0].finish_reason,
                    "model": response.model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
            else:
                logger.error("Unexpected response format")
                return {"error": "Invalid response format", "raw_response": str(response)}
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            return {"error": str(e), "raw_response": str(response)}

    def stream_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_message: str = "You are a helpful assistant."
    ):
        """
        Stream text generation responses.
        
        Args:
            prompt: The user prompt for text generation
            max_tokens: Maximum tokens in the response
            temperature: Sampling temperature (0.0-2.0)
            system_message: System message to set context
            
        Yields:
            Text chunks as they are generated
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
            yield f"\nError: {str(e)}"


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = OpenAIClient()
    
    # Example 1: Generate text
    try:
        response = client.generate_text(
            prompt="Explain quantum computing in simple terms.",
            system_message="You are a science educator who explains complex topics simply."
        )
        print("Generated text:")
        print(response["text"])
        print(f"\nUsage: {response['usage']['total_tokens']} tokens")
    except Exception as e:
        print(f"Error generating text: {str(e)}")
    
    # Example 2: Stream text
    print("\n--- Streaming Response ---")
    try:
        for text_chunk in client.stream_text(
            prompt="Write a short poem about technology.",
            temperature=0.9
        ):
            print(text_chunk, end="", flush=True)
    except Exception as e:
        print(f"\nError streaming text: {str(e)}")
