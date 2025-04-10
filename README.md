# Movie Review API

A RESTful API for movie reviews built with Django and Django REST Framework. This API allows users to search for movies, read and write reviews, and manage their profiles.

## Features

- User authentication via email/password or Google OAuth
- Movie search with integration to the OMDB API
- Create, read, update, and delete movie reviews
- User profile management
- JWT-based authentication
- Swagger API documentation
- Pagination and filtering

## Tech Stack

- Python 3.10+
- Django 5.2
- Django REST Framework
- SQLite (development)
- JWT Authentication (Simple JWT)
- Google OAuth2
- OMDB API integration

## Installation

### Prerequisites

- Python 3.10 or higher
- pip
- Git

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Kenward-dev/movie-review-api.git
   cd movie-review-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root directory with the following variables:
   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   OMDB_API_KEY=your_omdb_api_key
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```

6. Apply migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

| Variable | Description | How to Obtain |
|----------|-------------|---------------|
| SECRET_KEY | Django secret key | Generate one using `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| DEBUG | Debug mode (set to True for development) | N/A |
| OMDB_API_KEY | API key for OMDB API | Sign up at [OMDB API](http://www.omdbapi.com/apikey.aspx) |
| GOOGLE_CLIENT_ID | Google OAuth client ID | Create a project in the [Google Developer Console](https://console.developers.google.com/) |
| GOOGLE_CLIENT_SECRET | Google OAuth client secret | Create a project in the [Google Developer Console](https://console.developers.google.com/) |

## Authentication

The API supports two authentication methods:

### Email/Password Authentication (Recommended)

For most development and testing purposes, email/password authentication is simpler and recommended:

1. Create a user:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "securepassword", "first_name": "John", "last_name": "Doe"}'
   ```

2. Login to get JWT tokens:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "securepassword"}'
   ```

3. Use the access token in subsequent requests:
   ```bash
   curl -X GET http://127.0.0.1:8000/api/v1/movies/ \
     -H "Authorization: Bearer <your_access_token>"
   ```

### Google OAuth (Requires Frontend Integration)

Google OAuth is available but requires additional frontend integration:

1. Set up a Google OAuth consent screen in the Google Developer Console
2. Obtain a token from Google's OAuth flow
3. Send the token to the API:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/auth/google/ \
     -H "Content-Type: application/json" \
     -d '{"token": "<google_id_token>"}'
   ```

## API Documentation

The API documentation is available via Swagger UI when the application is running:

- Swagger UI: http://127.0.0.1:8000/api/v1/docs/
- ReDoc: http://127.0.0.1:8000/api/v1/redoc/

### Main Endpoints

| Endpoint | Method | Description | Authentication Required |
|----------|--------|-------------|------------------------|
| `/api/v1/auth/login/` | POST | Login with email/password | No |
| `/api/v1/auth/google/` | POST | Login with Google OAuth | No |
| `/api/v1/auth/me/` | GET | Get current user | Yes |
| `/api/v1/users/` | GET, POST | List or create users | GET: Yes, POST: No |
| `/api/v1/users/{id}/` | GET, PUT, PATCH, DELETE | Manage a specific user | Yes |
| `/api/v1/movies/` | GET | List movies | Yes |
| `/api/v1/movies/{id}/` | GET | Get a specific movie | Yes |
| `/api/v1/movies/search/q='movie_title'` | GET | Search for movies (local + OMDB) | Yes |
| `/api/v1/reviews/` | GET, POST | List or create reviews | Yes |
| `/api/v1/reviews/{id}/` | GET, PUT, PATCH, DELETE | Manage a specific review | Yes |
| `/api/v1/reviews/by-movie/` | GET | Get reviews for a specific movie | Yes |

## Usage Examples

### Creating a Movie Review

1. Search for a movie:
   ```bash
   curl -X GET "http://127.0.0.1:8000/api/v1/movies/search/?q=Inception" \
     -H "Authorization: Bearer <your_access_token>"
   ```

2. Create a review:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/reviews/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"movie_title": "Inception", "content": "A mind-bending masterpiece!", "rating": 5}'
   ```

3. Get reviews for a movie:
   ```bash
   curl -X GET "http://127.0.0.1:8000/api/v1/reviews/by-movie/?title=Inception" \
     -H "Authorization: Bearer <your_access_token>"
   ```

## Testing

### Running Tests

To run all tests:
```bash
python manage.py test
```

To run tests for a specific app:
```bash
python manage.py test authentication
python manage.py test movies
python manage.py test reviews
python manage.py test users
```


## Project Structure

```
movie_review_api/
├── authentication/       # Authentication related views and urls
├── movies/               # Movie model, views, serializers
├── movie_review_api/     # Project configuration
├── reviews/              # Review model, views, serializers
├── users/                # User model, views, serializers
├── utils/                # Shared utilities
├── manage.py
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [OMDB API](http://www.omdbapi.com/)