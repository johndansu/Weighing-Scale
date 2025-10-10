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
    from django.utils import timezone
    from datetime import datetime
    from django.db.models import Avg, Min, Max
    
    # Get all user's weight records
    all_records = WeightRecord.objects.filter(user=request.user)
    
    # Date filtering
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    
    filtered_records = all_records
    if date_from:
        filtered_records = filtered_records.filter(created_at__date__gte=date_from)
    if date_to:
        filtered_records = filtered_records.filter(created_at__date__lte=date_to)
    
    # Calculate total records
    total_records = all_records.count()
    
    # Calculate today's records
    today = timezone.now().date()
    today_records = all_records.filter(created_at__date=today).count()
    
    # Advanced statistics
    stats = all_records.aggregate(
        avg_weight=Avg('weight'),
        min_weight=Min('weight'),
        max_weight=Max('weight')
    )
    
    # Get recent 10 records for display (use filtered if dates are selected)
    weight_records = filtered_records.order_by('-created_at')[:10]
    
    context = {
        'weight_records': weight_records,
        'total_records': total_records,
        'today_records': today_records,
        'avg_weight': round(stats['avg_weight'], 2) if stats['avg_weight'] else 0,
        'min_weight': stats['min_weight'] if stats['min_weight'] else 0,
        'max_weight': stats['max_weight'] if stats['max_weight'] else 0,
    }
    
    return render(request, 'dashboard.html', context)

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
        weight = read_from_serial()  # Function to read weight from RS232
        return JsonResponse({'weight': weight})
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
                messages.success(request, f'Weight of {weight} kg recorded successfully!')
                return redirect('home')  # Redirect to the dashboard with name 'home'
            except ValueError:
                messages.error(request, 'Invalid weight value. Please enter a valid number.')
                return redirect('home')
            except Exception as e:
                print(f"Error saving weight: {e}")  # Print any error that occurs
                messages.error(request, 'An error occurred while saving your weight.')
                return redirect('home')
        else:
            messages.warning(request, 'No weight provided, and unable to read from the scale.')
            return redirect('home')
        
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

@login_required
def chart_data(request):
    from datetime import timedelta, datetime
    from django.utils import timezone
    from collections import defaultdict
    
    try:
        days = int(request.GET.get('days', 7))
        
        # Use TODAY as the reference point
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Get only records within the ACTUAL time period from today
        records = WeightRecord.objects.filter(
            user=request.user,
            created_at__gte=start_date,
            created_at__lte=end_date
        ).order_by('created_at')
        
        # Create dictionary to store weights by date for averaging
        weights_by_date = defaultdict(list)
        for record in records:
            date_key = record.created_at.date()
            weights_by_date[date_key].append(float(record.weight))
        
        # Generate complete date range with average per day
        date_labels = []
        weight_values = []
        
        current_date = start_date.date()
        end_date_only = end_date.date()
        found_first_data = False
        
        while current_date <= end_date_only:
            # Format date label
            date_labels.append(current_date.strftime('%b %d'))
            
            # Get AVERAGE weight for this date
            if current_date in weights_by_date:
                # Calculate average of all measurements on this day
                avg_weight = sum(weights_by_date[current_date]) / len(weights_by_date[current_date])
                weight_values.append(round(avg_weight, 1))
                found_first_data = True
            else:
                # Use 0 for days BEFORE first data, null for days AFTER
                if not found_first_data:
                    weight_values.append(0)  # Flat baseline at 0 before data
                else:
                    weight_values.append(None)  # Null after data
            
            current_date += timedelta(days=1)
        
        return JsonResponse({
            'dates': date_labels,
            'weights': weight_values,
            'count': len([w for w in weight_values if w is not None]),
            'period': f'Last {days} days',
            'total_days': len(date_labels)
        })
    except Exception as e:
        print(f"Chart data error: {e}")  # Debug print
        return JsonResponse({
            'dates': [],
            'weights': [],
            'error': str(e)
        }, status=500)

@login_required
def edit_record(request, record_id):
    import json
    if request.method == 'POST':
        try:
            record = WeightRecord.objects.get(id=record_id, user=request.user)
            data = json.loads(request.body)
            new_weight = float(data.get('weight'))
            record.weight = new_weight
            record.save()
            return JsonResponse({'success': True})
        except WeightRecord.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Record not found'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid weight value'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def delete_record(request, record_id):
    if request.method == 'POST':
        try:
            record = WeightRecord.objects.get(id=record_id, user=request.user)
            record.delete()
            return JsonResponse({'success': True})
        except WeightRecord.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Record not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def all_records(request):
    from django.core.paginator import Paginator
    
    # Get all records
    all_records = WeightRecord.objects.filter(user=request.user).order_by('-created_at')
    
    # Date filtering
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    
    if date_from:
        all_records = all_records.filter(created_at__date__gte=date_from)
    if date_to:
        all_records = all_records.filter(created_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(all_records, 20)  # 20 records per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'weight_records': page_obj,
        'total_records': all_records.count(),
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'all_records.html', context)
