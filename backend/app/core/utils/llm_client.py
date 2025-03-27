import os
import asyncio
import logging
import json
import httpx
import time
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("llm_client")

# Get environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "openai").lower()
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4") if DEFAULT_LLM_PROVIDER == "openai" else "claude-3-sonnet-20240229"

class LLMClient:
    """
    Client for communicating with Language Model APIs.
    Supports OpenAI and Anthropic models.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one LLM client exists."""
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the LLM client if not already initialized."""
        if not getattr(self, "_initialized", False):
            self.http_client = httpx.AsyncClient(timeout=60.0)
            self.api_keys = {
                "openai": OPENAI_API_KEY,
                "anthropic": ANTHROPIC_API_KEY
            }
            self.default_provider = DEFAULT_LLM_PROVIDER
            self.default_model = DEFAULT_MODEL
            self.request_count = 0
            self.total_tokens = 0
            self._initialized = True
            logger.info(f"LLM client initialized with default provider: {self.default_provider}")
    
    async def generate_text(
        self, 
        prompt: str, 
        model: Optional[str] = None, 
        provider: Optional[str] = None, 
        temperature: float = 0.2,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using a language model.
        
        Args:
            prompt: The prompt to send to the model
            model: Model name (defaults to environment variable)
            provider: Provider name (openai or anthropic, defaults to environment variable)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate (None for model default)
            
        Returns:
            Generated text
        """
        provider = provider or self.default_provider
        model = model or self.default_model
        
        self.request_count += 1
        logger.debug(f"Generating text with {provider}/{model} (request #{self.request_count})")
        
        # Choose the appropriate provider
        if provider == "openai":
            return await self._generate_openai(prompt, model, temperature, max_tokens)
        elif provider == "anthropic":
            return await self._generate_anthropic(prompt, model, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def _generate_openai(
        self, 
        prompt: str, 
        model: str, 
        temperature: float,
        max_tokens: Optional[int]
    ) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: The prompt to send to the model
            model: OpenAI model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        if not self.api_keys["openai"]:
            raise ValueError("OpenAI API key not configured")
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_keys['openai']}"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        start_time = time.time()
        
        try:
            async with self.http_client.stream("POST", url, json=payload, headers=headers) as response:
                response.raise_for_status()
                
                # Parse streaming response
                result = ""
                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line or line == "data: [DONE]":
                        continue
                    
                    if line.startswith("data: "):
                        try:
                            json_line = json.loads(line[6:])  # Remove 'data: ' prefix
                            if "choices" in json_line and len(json_line["choices"]) > 0:
                                delta = json_line["choices"][0].get("delta", {})
                                if "content" in delta:
                                    result += delta["content"]
                        except json.JSONDecodeError:
                            continue
                
                # Track token usage if available
                # This is approximate since we're streaming
                approx_tokens = len(prompt.split()) + len(result.split())
                self.total_tokens += approx_tokens
                
                logger.debug(f"OpenAI request completed in {time.time() - start_time:.2f}s")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from OpenAI: {e.response.status_code} {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error calling OpenAI: {str(e)}", exc_info=True)
            raise
    
    async def _generate_anthropic(
        self, 
        prompt: str, 
        model: str, 
        temperature: float,
        max_tokens: Optional[int]
    ) -> str:
        """
        Generate text using Anthropic API.
        
        Args:
            prompt: The prompt to send to the model
            model: Anthropic model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        if not self.api_keys["anthropic"]:
            raise ValueError("Anthropic API key not configured")
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": self.api_keys["anthropic"]
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        else:
            # Default to a reasonable limit
            payload["max_tokens"] = 4000
        
        start_time = time.time()
        
        try:
            response = await self.http_client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            text = result.get("content", [{"text": ""}])[0].get("text", "")
            
            # Track token usage if available
            if "usage" in result:
                input_tokens = result["usage"].get("input_tokens", 0)
                output_tokens = result["usage"].get("output_tokens", 0)
                self.total_tokens += input_tokens + output_tokens
            
            logger.debug(f"Anthropic request completed in {time.time() - start_time:.2f}s")
            return text
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from Anthropic: {e.response.status_code} {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error calling Anthropic: {str(e)}", exc_info=True)
            raise
    
    async def generate_embeddings(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        Currently only supports OpenAI embeddings.
        
        Args:
            texts: List of texts to generate embeddings for
            model: Embedding model name (defaults to "text-embedding-3-small")
            
        Returns:
            List of embedding vectors
        """
        if not self.api_keys["openai"]:
            raise ValueError("OpenAI API key not configured")
        
        model = model or "text-embedding-3-small"
        
        url = "https://api.openai.com/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_keys['openai']}"
        }
        
        payload = {
            "model": model,
            "input": texts
        }
        
        try:
            response = await self.http_client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            embeddings = [item["embedding"] for item in result["data"]]
            
            # Track token usage
            if "usage" in result:
                self.total_tokens += result["usage"].get("total_tokens", 0)
            
            return embeddings
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from OpenAI embeddings: {e.response.status_code} {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}", exc_info=True)
            raise
    
    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "request_count": self.request_count,
            "total_tokens": self.total_tokens,
            "provider": self.default_provider,
            "model": self.default_model
        }


def get_llm_client() -> LLMClient:
    """Get the LLM client singleton instance."""
    return LLMClient() 