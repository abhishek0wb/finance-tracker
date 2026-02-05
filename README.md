# Hisaab - Personal Finance Tracker

A modern, minimalist personal finance tracker built with Django, HTMX, and Tailwind CSS. Track expenses, set budgets, and manage your finances with a clean, professional interface.

## Features

- **Transaction Management** - Add, view, and search income/expense transactions
- **Budget Tracking** - Set monthly, yearly, or one-time budgets with visual progress indicators
- **Category System** - User-specific categories with icons and colors
- **Dashboard** - Financial overview with calendar and recent activity
- **Dark Mode** - Full dark mode support with localStorage persistence
- **HTMX Integration** - Dynamic interactions without page reloads
- **Responsive Design** - Works seamlessly on desktop and mobile

## Tech Stack

- **Backend**: Django 4.2, PostgreSQL
- **Frontend**: HTMX, Tailwind CSS, DaisyUI
- **Deployment**: Docker, Google Cloud Run ready

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (or use Docker)
- Node.js (for Tailwind CSS)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/hisaab-finance-tracker.git
cd hisaab-finance-tracker
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
npm install
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings (SECRET_KEY, database credentials)
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Build CSS**
```bash
npm run build
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Using Docker

Start PostgreSQL with Docker Compose:

```bash
docker-compose up -d
```

The database will be available on `localhost:5433`.

## Project Structure

```
hisaab-finance-tracker/
├── expenses/              # Main app
│   ├── models.py         # Category, Budget, Transaction models
│   ├── views.py          # View logic and HTMX endpoints
│   ├── urls.py           # URL routing
│   ├── signals.py        # Auto-create default categories
│   └── templates/        # HTML templates
├── users/                # Authentication app
├── finance_tracker/      # Project settings
├── static/               # Static files (CSS, JS)
├── templates/            # Global templates
├── docker/               # Docker configuration
└── requirements.txt      # Python dependencies
```

## Key Models

### Category
User-specific categories with customizable icons and colors.

### Transaction
Income and expense records linked to categories.

### Budget
Monthly, yearly, or one-time spending limits with automatic calculation of spent amounts and remaining budget.

## Development

### Run tests
```bash
python manage.py test
```

### Watch CSS changes
```bash
npm run dev
```

### Collect static files
```bash
python manage.py collectstatic
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Google Cloud Run.

Quick deploy:
```bash
./deploy.sh
```

## Environment Variables

Required variables in `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
USE_DOCKER=True

POSTGRES_DB=finance_tracker
POSTGRES_USER=finance_user
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- UI powered by [Tailwind CSS](https://tailwindcss.com/) and [DaisyUI](https://daisyui.com/)
- Dynamic interactions with [HTMX](https://htmx.org/)
