# Changelog

All notable changes to Codemni-ToolCallAgent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-24

### Added
- Initial release of Codemni-ToolCallAgent
- Support for multiple LLM providers:
  - OpenAI (GPT-4, GPT-3.5-turbo, etc.)
  - Anthropic (Claude-3-opus, Claude-3-sonnet, etc.)
  - Groq (Llama3-70b, Mixtral-8x7b, etc.)
  - Google (Gemini-pro, Gemini-1.5-pro, etc.)
  - Ollama (local models)
- Tool calling functionality with automatic parameter parsing
- Verbose mode with colored console output
- Zero required dependencies (all LLM providers are optional)
- Comprehensive examples and documentation
- Support for environment variable configuration
- Dynamic LLM provider switching
- Custom LLM integration support

### Features
- Intelligent tool selection based on user queries
- Automatic parameter extraction and validation
- Support for multiple tools per agent
- Iterative tool calling with scratchpad memory
- Error handling and validation
- Color-coded verbose output for debugging

### Documentation
- Comprehensive README with usage examples
- Example scripts for different use cases
- API reference documentation
- Publishing guide for package maintenance
- License and contribution guidelines

[1.0.0]: https://github.com/yourusername/Codemni-ToolCallAgent/releases/tag/v1.0.0
