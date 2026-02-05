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
- **Database**: PostgreSQL (Docker) or SQLite

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (optional, can use SQLite)
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
# Edit .env with your settings
```

Required `.env` variables:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
USE_DOCKER=False  # Set to True if using PostgreSQL with Docker
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

## Using PostgreSQL with Docker

If you want to use PostgreSQL instead of SQLite:

1. **Start PostgreSQL**
```bash
docker-compose up -d
```

2. **Update .env**
```env
USE_DOCKER=True
POSTGRES_DB=finance_tracker
POSTGRES_USER=finance_user
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

3. **Run migrations**
```bash
python manage.py migrate
```

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
└── docker/               # Docker configuration
```

## Key Features Explained

### Category System
- User-specific categories with customizable icons and colors
- 8 default categories created automatically for new users
- Categories can be shared across transactions and budgets

### Budget Tracking
- Set budgets with different periods: Monthly, Yearly, or One-Time
- Visual progress bars showing spending vs budget
- Color-coded status (green < 80%, yellow 80-99%, red 100%+)
- Automatic calculation of spent amounts for current period

### Transaction Management
- Quick add form with HTMX for instant updates
- Search functionality to filter by category or description
- Delete transactions with confirmation
- Automatic date assignment (today's date)

### Dark Mode
- Toggle between light and dark themes
- Preference saved in browser localStorage
- Smooth transitions between themes

## Development

### Watch CSS changes
```bash
npm run dev
```

### Run tests
```bash
python manage.py test
```

### Collect static files
```bash
python manage.py collectstatic
```

## Database Models

### Category
```python
- user: ForeignKey to User
- name: CharField (max 50)
- icon: CharField (Bootstrap icon name)
- color: CharField (hex color)
- created_at: DateTimeField
```

### Budget
```python
- user: ForeignKey to User
- category: ForeignKey to Category
- amount: DecimalField
- period: CharField (monthly/yearly/one-time)
- start_date: DateField
- created_at: DateTimeField
```

### Transaction
```python
- user: ForeignKey to User
- category: ForeignKey to Category (nullable)
- transaction_type: CharField (Income/Expense)
- amount: DecimalField
- date: DateField
- description: TextField (optional)
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

## Screenshots

*Coming soon - Add screenshots of your application here*

## Roadmap

- [ ] Add data export (CSV/Excel)
- [ ] Add charts and analytics
- [ ] Add recurring transactions
- [ ] Add multi-currency support
- [ ] Add mobile app (React Native)

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/hisaab-finance-tracker/issues).
