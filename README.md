# Weighing System

## Overview
The Weighing System is a Django-based web application that allows users to input, review, and manage their weight records. Users can manually enter their weights or capture them from a connected scale. The application also provides functionalities to export weight records in CSV format.

## Features
- User authentication (registration, login, logout).
- Input weight manually or capture from a scale.
- View and review the last 10 weight records.
- Export weight records in CSV format.
- User-friendly interface with responsive design.

## Technologies Used
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (or any other database of your choice)
- **Libraries**: Chart.js (for future enhancements)

## Installation

### Prerequisites
- Python 3.x
- Django 3.x or higher
- Virtual environment (recommended)

### Steps to Set Up
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/weighing-system.git
   cd weighing-system
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`.

## Usage
1. **Register** for an account.
2. **Log in** to access the dashboard.
3. **Input your weight** either manually or capture it from the scale.
4. **Review your last 10 weight records** displayed on the dashboard.
5. **Download your weight records** in CSV format.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Django Documentation for guidance.
- Chart.js for visualization capabilities.
- Community support and resources.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any enhancements or bug fixes.
