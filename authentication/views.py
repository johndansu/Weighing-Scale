from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from .models import WeightRecord
from .forms import WeightForm
from django.contrib import messages
from .serial_util import read_from_serial

# Create your views here.
@login_required
def dashboard(request):
    weight_records = WeightRecord.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'dashboard.html', {'weight_records': weight_records})

def weighing_process(request):
    if request.method == 'POST':
        # Handle manual weight input
        weight = request.POST.get('weight', 0)
        # Add logic to process the weight value (e.g., save to database)
        return HttpResponse(f"Weight {weight} kg recorded successfully!")

    # On GET, display the weighing form
    return render(request, 'weighing_process.html')

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True  # Optional: skip login if user is already logged in
    success_url = '/dashboard/'  # Specify the dashboard URL directly

# def custom_logout(request):
#     logout(request)  # This logs out the user
#     return redirect('login')


def custom_logout(request):
    logout(request)  # Log the user out
    return redirect('/')  # Redirect to your login page

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to a 'home' page or dashboard after signup
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'authentication/signup.html', {'form': form})
    

@login_required
def fetch_weight(request):
    if request.method == 'GET':
        weight = read_from_serial()  # Read weight from the RS232
        return JsonResponse({'weight': weight})  # Return the weight in JSON format
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def submit_weight(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')  # Get the weight from the POST request
        
        # If weight is not provided, try reading from the RS232
        if not weight:
            weight = read_from_serial()  # Read weight from the RS232
            
        if weight:  # Check if weight is provided
            try:
                WeightRecord.objects.create(user=request.user, weight=float(weight))  # Save the record
                return redirect('home')  # Redirect to the dashboard with name 'home'
            except Exception as e:
                print(f"Error saving weight: {e}")  # Print any error that occurs
                return HttpResponse("An error occurred while saving your weight.")  # Optional: send an error response
        else:
            return HttpResponse("No weight provided, and unable to read from the scale.")  # Handle case where no weight is read
        
    return render(request, 'dashboard.html')  # Render the dashboard if not POST

@login_required
def export_weights(request):
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_weights.csv"'

    writer = csv.writer(response)
    writer.writerow(['Record ID', 'Weight', 'Date'])  # Added Record ID header

    # Retrieve records and format the date
    records = WeightRecord.objects.filter(user=request.user)  # Get the full queryset
    for record in records:
        # Format date with AM/PM
        formatted_date = record.created_at.strftime('%Y-%m-%d %I:%M %p')
        writer.writerow([record.id, record.weight, formatted_date])  # Include record ID

    return response
