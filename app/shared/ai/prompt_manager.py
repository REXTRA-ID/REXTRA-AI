# app/shared/ai/prompt_manager.py
import os
import yaml
from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger()

class PromptManager:
    """
    Manajer Prompt untuk memuat dan mengelola template prompt AI dari file YAML.
    Mendukung pengorganisasian berdasarkan fitur (folder).
    """
    _instance = None
    _prompts: Dict[str, Dict[str, str]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PromptManager, cls).__new__(cls)
            cls._instance._load_all_prompts()
        return cls._instance

    def _load_all_prompts(self):
        """Memuat semua file .yaml dari folder app/prompts secara rekursif."""
        base_path = os.path.join(os.getcwd(), "app", "prompts")
        if not os.path.exists(base_path):
            logger.warning("prompt_manager_base_path_not_found", path=base_path)
            return

        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".yaml") or file.endswith(".yml"):
                    file_path = os.path.join(root, file)
                    # Gunakan path relatif sebagai namespace (misal: features/career_profile)
                    rel_path = os.path.relpath(file_path, base_path)
                    namespace = os.path.splitext(rel_path)[0].replace(os.sep, "/")
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = yaml.safe_load(f)
                            if data:
                                self._prompts[namespace] = data
                                logger.info("prompt_manager_loaded_namespace", namespace=namespace)
                    except Exception as e:
                        logger.error("prompt_manager_load_failed", file=file, error=str(e))

    def get_prompt(self, namespace: str, key: str, **kwargs) -> str:
        """
        Mengambil prompt dari namespace dan key tertentu, lalu memformatnya dengan kwargs.
        
        Contoh:
        manager.get_prompt("features/career_profile", "ikigai_scoring_batch", user_text="...")
        """
        namespace_data = self._prompts.get(namespace)
        if not namespace_data:
            logger.error("prompt_manager_namespace_not_found", namespace=namespace)
            raise ValueError(f"Namespace '{namespace}' tidak ditemukan.")

        prompt_template = namespace_data.get(key)
        if not prompt_template:
            logger.error("prompt_manager_key_not_found", namespace=namespace, key=key)
            raise ValueError(f"Key '{key}' tidak ditemukan di namespace '{namespace}'.")

        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            logger.error("prompt_manager_format_failed", namespace=namespace, key=key, missing_key=str(e))
            raise ValueError(f"Missing variable {str(e)} for prompt {namespace}/{key}")

# Singleton instance
prompt_manager = PromptManager()
