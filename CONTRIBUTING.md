# Contributing to Hisaab Finance Tracker

Thank you for considering contributing to Hisaab! This is a personal finance tracker built with Django, HTMX, and Tailwind CSS.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **Screenshots** if relevant
- **Environment details** (OS, Python version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Include:

- **Clear title** for the enhancement
- **Detailed description** of the suggested feature
- **Why this would be useful** to users
- **Examples** from other applications if applicable

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.9+
- PostgreSQL (optional, can use SQLite)
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

# Set up environment
cp .env.example .env
# Edit .env with: SECRET_KEY, DEBUG=True, USE_DOCKER=False

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Build CSS
npm run build

# Run server
python manage.py runserver
```

### Using Docker (Optional)

```bash
# Start PostgreSQL
docker-compose up -d

# Update .env with USE_DOCKER=True
# Run migrations
python manage.py migrate
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions and classes

### Django Best Practices

- Use class-based views where appropriate
- Keep views thin, models fat
- Always use `@login_required` for protected views
- Use Django's ORM (avoid raw SQL)

### Frontend Guidelines

- Use Tailwind CSS utility classes
- Follow existing design system
- Ensure responsive design (mobile-first)
- Test in both light and dark modes
- Use HTMX for dynamic interactions

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues after the first line

Example:
```
Add budget export to CSV feature

- Create export view and URL
- Add CSV generation logic
- Update budget page with export button

Closes #42
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test expenses
```

## Project Structure

```
hisaab-finance-tracker/
├── expenses/           # Main app
│   ├── models.py      # Database models
│   ├── views.py       # View logic
│   ├── urls.py        # URL routing
│   └── templates/     # HTML templates
├── users/             # Authentication
├── finance_tracker/   # Project settings
├── static/            # CSS, JS
└── templates/         # Global templates
```

## What to Contribute

### Good First Issues

- Add more default categories
- Improve error messages
- Add form validation
- Write tests
- Fix UI bugs
- Improve documentation

### Feature Ideas

- Data export (CSV/Excel)
- Charts and analytics
- Recurring transactions
- Multi-currency support
- Budget alerts
- Transaction tags

## Questions?

- Open an issue with the "question" label
- Check existing documentation
- Review closed issues

Thank you for contributing! 🎉
