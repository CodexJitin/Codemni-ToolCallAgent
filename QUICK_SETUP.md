# Quick Setup Guide

Follow these steps to prepare and publish your package:

## 1. Install Build Tools
```powershell
pip install build twine
```

## 2. Build the Package
```powershell
# Clean previous builds
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# Build
python -m build
```

## 3. Test Locally
```powershell
# Install in development mode
pip install -e .

# Or install from wheel
pip install dist/Codemni_ToolCallAgent-1.0.0-py3-none-any.whl

# Run test script
python test_package.py
```

## 4. Test with Examples
```powershell
cd examples
python basic_usage.py
```

## 5. Publish to PyPI

### First time setup:
1. Create account at https://pypi.org
2. Generate API token
3. Save token securely

### Upload:
```powershell
# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token

## 6. Verify Installation
```powershell
# In a new environment
pip install Codemni-ToolCallAgent

# Test it
python -c "from ToolCall_Agent import ToolCallAgent; print('Success!')"
```

## Package Structure
```
x:\
├── agent/
│   └── ToolCall_Agent/
│       ├── __init__.py          # Package initialization
│       ├── agent.py             # Main agent class
│       ├── llm_providers.py     # LLM provider wrappers
│       └── prompt.py            # Prompt template
├── examples/                     # Usage examples
│   ├── basic_usage.py
│   ├── multiple_tools.py
│   ├── different_llm_providers.py
│   └── README.md
├── setup.py                      # Setup configuration
├── pyproject.toml               # Modern Python packaging
├── README.md                     # Package documentation
├── LICENSE                       # MIT License
├── CHANGELOG.md                  # Version history
├── MANIFEST.in                   # Include additional files
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Dependencies
├── PUBLISHING.md                 # Detailed publishing guide
└── test_package.py              # Verification script

```

## Next Steps

1. **Update URLs**: Edit `setup.py` and `pyproject.toml` to add your GitHub repository URL
2. **Add Email**: Add your email in `setup.py`
3. **Test Everything**: Run through examples and tests
4. **Publish**: Follow the publishing guide in PUBLISHING.md

For detailed instructions, see **PUBLISHING.md**
