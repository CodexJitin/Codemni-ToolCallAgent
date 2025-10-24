# Publishing Guide for Codemni-ToolCallAgent

This guide explains how to build and publish the package to PyPI.

## Prerequisites

1. Install required build tools:
```bash
pip install build twine
```

2. Create accounts:
   - [PyPI Account](https://pypi.org/account/register/)
   - [TestPyPI Account](https://test.pypi.org/account/register/) (optional, for testing)

3. Set up API tokens:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Generate an API token
   - Save it securely

## Building the Package

1. Clean previous builds:
```bash
# On Windows (PowerShell)
Remove-Item -Recurse -Force build, dist, *.egg-info

# On Linux/Mac
rm -rf build/ dist/ *.egg-info
```

2. Build the distribution packages:
```bash
python -m build
```

This creates:
- `dist/Codemni-ToolCallAgent-1.0.0.tar.gz` (source distribution)
- `dist/Codemni_ToolCallAgent-1.0.0-py3-none-any.whl` (wheel distribution)

## Testing the Package Locally

Install the package locally to test:

```bash
pip install -e .
```

Or install from the built wheel:

```bash
pip install dist/Codemni_ToolCallAgent-1.0.0-py3-none-any.whl
```

## Publishing to TestPyPI (Optional but Recommended)

Test your package on TestPyPI first:

```bash
python -m twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: Your TestPyPI API token (starts with `pypi-`)

Install from TestPyPI to test:

```bash
pip install --index-url https://test.pypi.org/simple/ Codemni-ToolCallAgent
```

## Publishing to PyPI

Once you've tested everything:

```bash
python -m twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pypi-`)

## Using .pypirc (Alternative)

Create `~/.pypirc` file to avoid entering credentials each time:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

**Important:** Keep this file secure and never commit it to version control!

Then upload with:

```bash
# To TestPyPI
twine upload -r testpypi dist/*

# To PyPI
twine upload -r pypi dist/*
```

## Complete Workflow

Here's the complete workflow for publishing:

```bash
# 1. Clean previous builds
Remove-Item -Recurse -Force build, dist, *.egg-info

# 2. Build the package
python -m build

# 3. Check the distribution
twine check dist/*

# 4. Upload to TestPyPI (optional)
twine upload --repository testpypi dist/*

# 5. Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ Codemni-ToolCallAgent

# 6. If everything works, upload to PyPI
twine upload dist/*

# 7. Test install from PyPI
pip install Codemni-ToolCallAgent
```

## Updating the Package

When you need to release a new version:

1. Update version in `setup.py` and `pyproject.toml`
2. Update version in `agent/ToolCall_Agent/__init__.py`
3. Update CHANGELOG (if you have one)
4. Build and publish following the steps above

## Checking the Package

Before uploading, check your package:

```bash
# Check distribution files
twine check dist/*

# View package metadata
tar -tzf dist/Codemni-ToolCallAgent-1.0.0.tar.gz

# Or for wheel
unzip -l dist/Codemni_ToolCallAgent-1.0.0-py3-none-any.whl
```

## Troubleshooting

### "File already exists" error
This means you're trying to upload a version that already exists. You need to:
1. Increment the version number
2. Rebuild the package
3. Upload again

### Import errors after installation
Make sure your package structure is correct:
- Check that `__init__.py` exists in the package directory
- Verify `find_packages()` finds your package
- Test local installation with `pip install -e .`

### Missing dependencies
Users should install with extras:
```bash
pip install Codemni-ToolCallAgent[openai]  # For specific provider
pip install Codemni-ToolCallAgent[all]     # For all providers
```

## Best Practices

1. **Always test locally first**: `pip install -e .`
2. **Test on TestPyPI before PyPI**: Catch issues early
3. **Use semantic versioning**: MAJOR.MINOR.PATCH (e.g., 1.0.0, 1.0.1, 1.1.0)
4. **Keep a CHANGELOG**: Document what changed in each version
5. **Tag releases in git**: `git tag -a v1.0.0 -m "Release 1.0.0"`
6. **Update documentation**: Keep README.md current

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI](https://pypi.org/)
- [TestPyPI](https://test.pypi.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
