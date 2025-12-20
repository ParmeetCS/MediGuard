"""
Google ADK Runtime - MediGuard Drift AI
Central execution layer for Google's Agent Development Kit (ADK)
Handles Gemini model initialization and agent prompt execution
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional, Dict, List, Any
import streamlit as st

# ========================================
# LOAD ENVIRONMENT VARIABLES
# ========================================
load_dotenv()

# Get Google API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ========================================
# GEMINI MODEL CONFIGURATION
# ========================================

# Default model configuration following ADK best practices
DEFAULT_MODEL_CONFIG = {
    "temperature": 0.7,  # Balance between creativity and consistency
    "top_p": 0.95,       # Nucleus sampling for diverse responses
    "top_k": 40,         # Top-k sampling for quality
    "max_output_tokens": 2048,  # Maximum response length
}

# Safety settings for health-related content
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]


class GeminiADKRuntime:
    """
    Google ADK Runtime for MediGuard Drift AI
    
    This class encapsulates the Gemini AI model and provides
    a clean interface for agent-based interactions following
    Google's ADK design principles.
    """
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the ADK runtime with Gemini model
        
        Args:
            model_name (str): Gemini model to use (default: gemini-1.5-flash)
        """
        self.model_name = model_name
        self.model = None
        self.is_configured = False
        
        # Configure the runtime
        self._configure()
    
    def _configure(self) -> None:
        """
        Configure Google Generative AI with API key
        Internal method called during initialization
        """
        if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_real_key_here":
            print("Warning: Google API key not configured. Set GOOGLE_API_KEY in .env file.")
            self.is_configured = False
            return
        
        try:
            # Configure the Google Generative AI library
            genai.configure(api_key=GOOGLE_API_KEY)
            
            # Initialize the Gemini model with safety settings
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                safety_settings=SAFETY_SETTINGS
            )
            
            self.is_configured = True
            print(f"✅ ADK Runtime initialized with model: {self.model_name}")
            
        except Exception as e:
            print(f"❌ Error configuring ADK Runtime: {str(e)}")
            self.is_configured = False
    
    def run_agent_prompt(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute an agent prompt using Gemini model
        
        This is the core ADK execution method that processes agent requests
        following Google's ADK design principles.
        
        Args:
            prompt (str): User prompt or agent query
            system_instruction (str, optional): System-level instructions for the agent
            config (dict, optional): Custom generation config (overrides defaults)
        
        Returns:
            Dict containing:
                - success (bool): Whether the request succeeded
                - response (str): Generated response text
                - error (str): Error message if failed
                - metadata (dict): Additional response metadata
        
        Example:
            result = runtime.run_agent_prompt(
                prompt="Analyze this health trend data...",
                system_instruction="You are a health monitoring AI assistant."
            )
            
            if result['success']:
                print(result['response'])
        """
        if not self.is_configured:
            return {
                "success": False,
                "response": "",
                "error": "ADK Runtime not configured. Please set GOOGLE_API_KEY in .env file.",
                "metadata": {}
            }
        
        if not prompt:
            return {
                "success": False,
                "response": "",
                "error": "Prompt cannot be empty.",
                "metadata": {}
            }
        
        try:
            # Use custom config or defaults
            generation_config = config if config else DEFAULT_MODEL_CONFIG
            
            # Construct full prompt with system instruction if provided
            full_prompt = prompt
            if system_instruction:
                full_prompt = f"{system_instruction}\n\n{prompt}"
            
            # Generate response using Gemini
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            # Extract response text
            response_text = response.text if hasattr(response, 'text') else ""
            
            # Prepare metadata
            metadata = {
                "model": self.model_name,
                "prompt_length": len(prompt),
                "response_length": len(response_text),
                "finish_reason": getattr(response, 'finish_reason', None) if hasattr(response, 'candidates') else None
            }
            
            return {
                "success": True,
                "response": response_text,
                "error": None,
                "metadata": metadata
            }
            
        except Exception as e:
            error_message = str(e)
            
            # Handle specific error cases
            if "API key not valid" in error_message:
                error_message = "Invalid Google API key. Please check your .env configuration."
            elif "quota" in error_message.lower():
                error_message = "API quota exceeded. Please try again later or upgrade your plan."
            elif "safety" in error_message.lower():
                error_message = "Response blocked by safety filters. Please rephrase your request."
            
            return {
                "success": False,
                "response": "",
                "error": error_message,
                "metadata": {}
            }
    
    def run_agent_chat(
        self,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a multi-turn conversation using chat interface
        
        Args:
            messages (list): List of message dicts with 'role' and 'content'
            system_instruction (str, optional): System-level instructions
        
        Returns:
            Dict containing success status, response, and metadata
        
        Example:
            messages = [
                {"role": "user", "content": "What is my stability trend?"},
                {"role": "assistant", "content": "Your stability has declined by 4%..."},
                {"role": "user", "content": "What should I do?"}
            ]
            result = runtime.run_agent_chat(messages)
        """
        if not self.is_configured:
            return {
                "success": False,
                "response": "",
                "error": "ADK Runtime not configured.",
                "metadata": {}
            }
        
        try:
            # Start chat session
            chat = self.model.start_chat(history=[])
            
            # Add system instruction as first message if provided
            if system_instruction:
                chat.send_message(f"System: {system_instruction}")
            
            # Process message history
            for msg in messages[:-1]:  # All but last message
                if msg['role'] == 'user':
                    chat.send_message(msg['content'])
            
            # Send final message and get response
            last_message = messages[-1]['content']
            response = chat.send_message(last_message)
            
            response_text = response.text if hasattr(response, 'text') else ""
            
            return {
                "success": True,
                "response": response_text,
                "error": None,
                "metadata": {
                    "model": self.model_name,
                    "messages_count": len(messages)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": "",
                "error": str(e),
                "metadata": {}
            }
    
    def is_ready(self) -> bool:
        """
        Check if ADK runtime is ready for use
        
        Returns:
            bool: True if configured and ready, False otherwise
        """
        return self.is_configured


# ========================================
# GLOBAL RUNTIME INSTANCE
# ========================================

# Create a single shared instance for the application
# This follows the singleton pattern for efficient resource usage
adk_runtime = GeminiADKRuntime()


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def run_agent(prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to run an agent prompt using the global runtime
    
    Args:
        prompt (str): User prompt
        system_instruction (str, optional): System instruction
    
    Returns:
        Dict: Response dictionary
    
    Example:
        result = run_agent("Explain my health drift pattern")
        if result['success']:
            print(result['response'])
    """
    return adk_runtime.run_agent_prompt(prompt, system_instruction)


def is_adk_ready() -> bool:
    """
    Check if ADK is ready for use
    
    Returns:
        bool: True if ready
    """
    return adk_runtime.is_ready()


def get_runtime() -> GeminiADKRuntime:
    """
    Get the global ADK runtime instance
    
    Returns:
        GeminiADKRuntime: The runtime instance
    """
    return adk_runtime
