# Contributing to Hisaab Finance Tracker

First off, thank you for considering contributing to Hisaab! It's people like you that make Hisaab such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if relevant**
- **Include your environment details** (OS, Python version, Django version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other applications**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Set up your development environment** (see below)
3. **Make your changes** following our coding standards
4. **Add tests** for any new functionality
5. **Ensure all tests pass**
6. **Update documentation** as needed
7. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.9+
- PostgreSQL (or use Docker)
- Node.js (for Tailwind CSS)

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hisaab-finance-tracker.git
cd hisaab-finance-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Build Tailwind CSS
npm run build

# Run development server
python manage.py runserver
```

### Using Docker

```bash
# Start PostgreSQL
docker-compose up -d

# Run migrations
python manage.py migrate

# Start development
python manage.py runserver
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes

### Django Best Practices

- Use class-based views where appropriate
- Keep views thin, models fat
- Use Django's built-in authentication
- Always use `@login_required` for protected views
- Use Django's ORM, avoid raw SQL when possible

### Frontend Guidelines

- Use Tailwind CSS utility classes
- Follow the existing design system
- Ensure responsive design (mobile-first)
- Test in both light and dark modes
- Use HTMX for dynamic interactions

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line

Example:
```
Add monthly budget summary feature

- Create new view for monthly summaries
- Add chart visualization using Chart.js
- Update dashboard to show summary card

Closes #123
```

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test expenses

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Test both success and failure cases
- Use descriptive test names

Example:
```python
def test_user_can_create_budget_with_valid_data(self):
    """Test that authenticated user can create a budget"""
    # Test implementation
```

## Project Structure

```
hisaab-finance-tracker/
├── expenses/           # Main app for transactions and budgets
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   ├── urls.py        # URL routing
│   └── templates/     # HTML templates
├── users/             # User authentication app
├── finance_tracker/   # Project settings
├── static/            # Static files (CSS, JS)
├── templates/         # Global templates
└── tests/             # Test files
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions and classes
- Update DEPLOYMENT.md for infrastructure changes
- Create/update docs/ files for major features

## Review Process

1. **Automated checks** must pass (tests, linting)
2. **Code review** by at least one maintainer
3. **Documentation** must be updated
4. **Tests** must be included for new features

## Questions?

Feel free to:
- Open an issue with the "question" label
- Reach out to maintainers
- Check existing documentation

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to Hisaab! 🎉
