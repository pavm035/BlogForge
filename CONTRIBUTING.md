# Contributing to BlogForge

Thank you for your interest in contributing to BlogForge! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/blogforge.git
   cd blogforge
   ```
3. **Set up development environment**
   ```bash
   uv sync
   cp .env.example .env
   # Add your API keys to .env
   ```

## 🔧 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Follow the existing code style
- Add tests if applicable
- Update documentation as needed
- Keep commits atomic and well-described

### 3. Test Your Changes

```bash
# Run the application
uv run main.py

# Test the API
curl -X POST "http://localhost:8000/blog/" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Test Topic"}'
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
# or
git commit -m "fix: fix your bug description"
```

**Commit Message Format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📝 Code Style

- Use **Python 3.13+** features where appropriate
- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and returns
- Use **Pydantic models** for data validation
- Add **docstrings** to all classes and functions
- Keep functions **focused and small**

### Example Code Style

```python
from pydantic import BaseModel, Field
from typing import Dict, Any

class MyModel(BaseModel):
    """
    A clear description of what this model represents.
    
    Attributes:
        field_name: Description of the field
    """
    
    field_name: str = Field(
        ...,
        description="Clear description",
        min_length=1
    )
    
    def my_method(self, param: str) -> Dict[str, Any]:
        """
        Clear description of what this method does.
        
        Args:
            param: Description of parameter
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When something goes wrong
        """
        if not param:
            raise ValueError("Parameter cannot be empty")
        
        return {"result": param}
```

## 🧪 Testing Guidelines

- Test your changes manually before submitting
- Ensure the API starts without errors
- Test with different languages if applicable
- Verify the API documentation at `/docs` works correctly

## 📚 Documentation

- Update `README.md` if you add new features
- Add docstrings to all new functions/classes
- Update `.env.example` if you add new environment variables
- Keep documentation clear and concise

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description** - Clear description of the issue
2. **Steps to Reproduce** - Exact steps to reproduce the bug
3. **Expected Behavior** - What you expected to happen
4. **Actual Behavior** - What actually happened
5. **Environment** - Python version, OS, etc.
6. **Logs** - Relevant error messages or logs

## 💡 Feature Requests

When requesting features:

1. **Use Case** - Explain why this feature would be useful
2. **Proposed Solution** - How you think it should work
3. **Alternatives** - Other solutions you've considered

## ✅ Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows the project's style guidelines
- [ ] All existing tests pass
- [ ] New features include documentation
- [ ] Commit messages are clear and descriptive
- [ ] No sensitive data (API keys, passwords) in commits
- [ ] `.gitignore` is properly configured
- [ ] The application runs without errors

## 🤝 Code Review Process

1. A maintainer will review your PR
2. They may request changes or improvements
3. Make the requested changes
4. Once approved, your PR will be merged

## 📞 Questions?

- Open a [Discussion](https://github.com/yourusername/blogforge/discussions)
- Ask in the [Issues](https://github.com/yourusername/blogforge/issues)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to BlogForge! 🎉
