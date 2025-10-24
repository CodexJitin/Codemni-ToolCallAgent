"""
Setup configuration for Codemni-ToolCallAgent
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="Codemni-ToolCallAgent",
    version="1.0.0",
    author="CodexJitin",
    author_email="codexjitin@gmail.com",
    description="An intelligent agent that can call tools based on LLM decisions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Codexjitin/Codemni-ToolCallAgent",
    packages=find_packages(where="agent"),
    package_dir={"": "agent"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies - none required, all LLM providers are optional
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.18.0"],
        "groq": ["groq>=0.4.0"],
        "google": ["google-generativeai>=0.3.0"],
        "ollama": ["ollama>=0.1.0"],
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.18.0",
            "groq>=0.4.0",
            "google-generativeai>=0.3.0",
            "ollama>=0.1.0",
        ],
    },
    keywords="ai agent llm tool-calling openai anthropic groq ollama gemini",
    project_urls={
        "Bug Reports": "https://github.com/Codexjitin/Codemni-ToolCallAgent/issues",
        "Source": "https://github.com/Codexjitin/Codemni-ToolCallAgent",
        "Documentation": "https://github.com/Codexjitin/Codemni-ToolCallAgent#readme",
    },
)
