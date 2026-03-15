# app/shared/ai/base.py
import json
import structlog
from typing import Dict, Any, Optional, List
from app.shared.ai_client import gemini_client
from app.shared.ai.prompt_manager import prompt_manager

logger = structlog.get_logger()

class BaseAIService:
    """
    Base class untuk semua AI Services.
    Menyediakan integrasi otomatis dengan PromptManager dan GeminiClient.
    """
    
    def __init__(self, namespace: str):
        self.namespace = namespace
        self.client = gemini_client
        self.prompt_manager = prompt_manager

    def _get_formatted_prompt(self, key: str, **kwargs) -> str:
        """Mengambil dan memformat prompt dari PromptManager."""
        return self.prompt_manager.get_prompt(self.namespace, key, **kwargs)

    async def call_ai(
        self, 
        prompt_key: str, 
        prompt_vars: Dict[str, Any], 
        max_tokens: int = 2000, 
        temperature: float = 0.7,
        dimension: str = "general"
    ) -> str:
        """
        Memanggil AI dengan prompt dari template.
        """
        prompt_content = self._get_formatted_prompt(prompt_key, **prompt_vars)
        messages = [{"role": "user", "content": prompt_content}]
        
        return await self.client.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            dimension=dimension
        )

    async def call_ai_json(
        self, 
        prompt_key: str, 
        prompt_vars: Dict[str, Any], 
        max_tokens: int = 2000, 
        temperature: float = 0.1,
        dimension: str = "general"
    ) -> Any:
        """
        Memanggil AI dan mengharapkan response JSON.
        Otomatis melakukan stripping markdown dan parsing JSON.
        """
        raw_response = await self.call_ai(
            prompt_key=prompt_key,
            prompt_vars=prompt_vars,
            max_tokens=max_tokens,
            temperature=temperature,
            dimension=dimension
        )
        
        cleaned = self.client._clean_json_response(raw_response)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error("ai_base_json_parse_failed", 
                         namespace=self.namespace, 
                         prompt_key=prompt_key, 
                         error=str(e))
            raise ValueError(f"AI response is not a valid JSON: {str(e)}")
