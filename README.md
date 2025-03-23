# Finance Tracker

## Overview
This project is a Django-based web application designed to help users manage and track their finances. The application includes features for adding, viewing, and analyzing transactions, setting budgets, and managing user accounts. The project is structured to follow Django's best practices, making it modular, scalable, and easy to maintain.

## Features
- **User Authentication:** Users can register, log in, and manage their accounts securely.
- **Transaction Management:** Add, edit, and view transactions categorized by type.
- **Budget Visualization:** View budgets and analyze spending patterns.
- **Dashboard:** An intuitive dashboard summarizing key financial data.
- **Responsive Templates:** Clean and user-friendly HTML templates for a seamless user experience.

## Setup Instructions
### Prerequisites
- Python 3.8 or higher
- Django 4.0 or higher
- Virtual environment (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd finance_tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/` in your browser.

## Deployment
The project includes a `Procfile` and `build.sh` script for deployment on platforms like Heroku. Ensure you configure environment variables such as `SECRET_KEY`, `DEBUG`, and database settings in the production environment.

## Testing
Run the test suite using:
```bash
python manage.py test
```

## Future Enhancements
- Add support for exporting transactions to CSV/Excel.
- Implement notifications for budget limits.
- Add multi-currency support.

## License
This project is licensed under the MIT License. Feel free to modify and use it as per your requirements.

