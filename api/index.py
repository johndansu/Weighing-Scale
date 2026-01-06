"""
Vercel serverless function entry point for Django application.
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weighing.settings")

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Initialize Django application
django_app = get_wsgi_application()

# Wrap with StaticFilesHandler for serving static files in development
# In production, static files should be served by Vercel
if os.environ.get("DEBUG", "False") == "True":
    django_app = StaticFilesHandler(django_app)

def handler(request):
    """
    Vercel serverless function handler.
    Converts Vercel request to Django WSGI request and returns response.
    """
    from django.core.handlers.wsgi import WSGIRequest
    from io import BytesIO
    
    # Get request body
    body = b''
    if hasattr(request, 'body'):
        body = request.body if isinstance(request.body, bytes) else request.body.encode()
    elif hasattr(request, 'read'):
        body = request.read()
    
    # Create WSGI environment
    environ = {
        'REQUEST_METHOD': getattr(request, 'method', 'GET'),
        'PATH_INFO': getattr(request, 'path', '/'),
        'QUERY_STRING': getattr(request, 'query_string', ''),
        'CONTENT_TYPE': getattr(request, 'headers', {}).get('Content-Type', ''),
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.input': BytesIO(body),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'SERVER_NAME': getattr(request, 'headers', {}).get('Host', 'localhost'),
        'SERVER_PORT': '443',
    }
    
    # Add HTTP headers
    headers = getattr(request, 'headers', {})
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    # Create Django request and get response
    django_request = WSGIRequest(environ)
    response = django_app(django_request)
    
    # Convert Django response to Vercel format
    return {
        'statusCode': response.status_code,
        'headers': dict(response.items()),
        'body': response.content.decode('utf-8') if isinstance(response.content, bytes) else str(response.content)
    }
