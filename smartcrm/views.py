from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Deal, Task, Lead, Activity
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from .serializers import LeadSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import LeadForm, ActivityForm, TaskForm, DealForm
from django.contrib import messages


# Create your views here.


@login_required
def index(request):
    # Fetch only the leads belonging to the logged-in user
    user_leads = Lead.objects.filter(owner=request.user).order_by('-created_at')
    user_deals = Deal.objects.filter(owner=request.user)
    urgent_tasks = Task.objects.filter(owner=request.user, is_completed=False).select_related('deal', 'deal__lead').order_by('due_date')[:5]
    total_leads = Lead.objects.filter(owner=request.user).count()
    recent_activities = Activity.objects.order_by('-created_at')[:5].values(
        'lead__first_name', 'lead__last_name', 'note', 'created_at'
    )
    recent_leads = Lead.objects.filter(owner=request.user).order_by('-created_at')[:5]

    deal_count = user_deals.count()
    lead_count = user_leads.count()

    


    total_sales = user_deals.aggregate(total=Sum('amount'))['total'] or 0

    # Define the context dictionary to pass variables to HTML
    context = {
        "lead_count": lead_count,
        "deal_count": deal_count,
        "total_sales": float(total_sales),
        "user_tasks": urgent_tasks,
        "recent_leads": user_leads.order_by('-created_at')[:5],
        "recent_activities": recent_activities,
    }

    
    return render(request, 'smartcrm/index.html', context)

@login_required
def dashboard_data(request):
   
    try:
        user_leads = Lead.objects.filter(owner=request.user)
        user_deals = Deal.objects.filter(owner=request.user)
        user_tasks = Task.objects.filter(owner=request.user, is_completed=False)
        
        # This line requires the 'Sum' import above
        total_sales = user_deals.aggregate(total=Sum('amount'))['total'] or 0

        data = {
            "lead_count": user_leads.count(),
            "deal_count": user_deals.count(),
            "total_sales": float(total_sales),
            "pending_tasks": user_tasks.count(),
        }
        return JsonResponse(data)
        
    except Exception as e:
      
        return JsonResponse({"error": str(e)}, status=500)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "smartcrm/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "smartcrm/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Basic Validation
        if password != confirmation:
            return render(request, "smartcrm/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "smartcrm/register.html", {"message": "Username already taken."})
        
        login(request, user)
        return redirect("index")
    else:
        return render(request, "smartcrm/register.html")

@login_required
def lead(request):
    lead = Lead.objects.all().order_by('-id')

        # Handle Search Query
    query = request.GET.get('q')
    if query:
        lead = lead.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(company__icontains=query) |
            Q(industry__icontains=query) |
            Q(status__icontains=query)
        )

    # Handle Pagination (Show 10 leads per page)
    paginator = Paginator(lead, 10) 
    page_number = request.GET.get('page')

    try:
        leads = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer (e.g. page=abc), deliver first page.
        leads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. page=9999), deliver last page of results.
        leads = paginator.page(paginator.num_pages)

    return render(request, "smartcrm/lead.html", {
        "leads": leads
    }) 


@login_required
def add_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.owner = request.user 
            lead.save()
            return JsonResponse({
                "message": "Lead added successfully!",
                "lead": {
                    "first_name": lead.first_name,
                    "last_name": lead.last_name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "company": lead.company,
                    "industry": lead.industry,
                    "status": lead.get_status_display(),
                    "created_at": lead.created_at.strftime("%b %d, %Y, %I:%M %p")
                }
            }, status=201)
        return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
    

    form = LeadForm()
    
    return render(request, 'smartcrm/add_lead.html', {'form': form})

@login_required
def edit_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            # Redirect straight back to the list here too
            return redirect('lead') 
    else:
        form = LeadForm(instance=lead)
        
    return render(request, 'smartcrm/add_lead.html', {'form': form})

    
@login_required
def lead_detail(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id, owner=request.user)

    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.lead = lead  
            activity.save()
            messages.success(request, "Activity logged!")
            return redirect('lead_detail', lead_id=lead_id)
    else:
        form = ActivityForm()

    activities = lead.activities.all().order_by('-created_at')

    context = {
        'lead': lead,
        'stage_choices': Deal.STAGE_CHOICES, # Send the choices tuple to HTML
        'activities': activities,
        'form': form
    }

    return render(request, 'smartcrm/lead_detail.html', context)

@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, "Note deleted successfully.")
    
    # Redirect back to the customer's profile page
    return redirect('lead_detail', lead_id=activity.lead.id)



@login_required
def delete_lead(request, lead_id):
    if request.method == "POST":
        lead = get_object_or_404(Lead, id=lead_id)
        lead.delete()
        return redirect('lead') 
        
    return redirect('lead')

@login_required
def delete_multiple_leads(request):
    if request.method == "POST":
        # Get the list of all checked lead IDs from the form
        lead_ids = request.POST.getlist('lead_ids')
        
        if lead_ids:
            # Delete all matching leads at once efficiently
            Lead.objects.filter(id__in=lead_ids).delete()
            
    return redirect('lead') 


@login_required
def convert_to_deal(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id, owner=request.user)
    

    if lead.status == "converted":
        messages.error(request, "This lead has already been converted into a deal and cannot be converted again.")
        return redirect('lead_detail', id=lead.id) # Send them back safely

    if request.method == "POST":

        deal = Deal.objects.create(
            owner=request.user,
            lead=lead,
            amount=request.POST.get('amount'),
            stage=request.POST.get('stage'),
            expected_close_date=request.POST.get('expected_close_date'),
            status="open"
        )
        
        lead.tasks.update(deal=deal)
        
        lead.status = "converted" 
        lead.save() 
        
        messages.success(request, f"Successfully created a deal for {lead.company}!")
        return redirect('deal_profile', deal_id=deal.id)
        
    return redirect('lead_detail', id=lead.id)

@login_required
def deal_profile(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id, owner=request.user)

    deal_tasks = Task.objects.filter(deal=deal).order_by('-created_at')

    context = {
        'deal': deal,
        'form': TaskForm(),
        'pending_tasks': deal_tasks.filter(is_completed=False),
        'completed_tasks': deal_tasks.filter(is_completed=True),
    }

    return render(request, 'smartcrm/deal_detail.html', context)

@login_required
def deals_dashboard(request):
    # Fetch all deals for the user, grouped by status
    open_deals = Deal.objects.filter(owner=request.user, status="open").select_related('lead')
    won_deals = Deal.objects.filter(owner=request.user, status="won").select_related('lead')
    lost_deals = Deal.objects.filter(owner=request.user, status="lost").select_related('lead')
    
    context = {
        'open_deals': open_deals,
        'won_deals': won_deals,
        'lost_deals': lost_deals,
    }
    return render(request, 'smartcrm/deals_list.html', context)

@login_required
def update_deal_status(request, deal_id, status_choice):
    deal = get_object_or_404(Deal, id=deal_id, owner=request.user)

    if status_choice in ['won', 'lost', 'open']:
        deal.status = status_choice
        deal.save()
        
         # Safe AJAX detection supporting vanilla fetch requests
        is_ajax = (
            request.headers.get('x-requested-with') == 'XMLHttpRequest' or 
            request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or
            request.content_type == 'application/json'
        )
        
        if is_ajax:
            return JsonResponse({
                'status': 'success', 
                'deal_id': deal_id, 
                'new_status': status_choice
            })
            
        # Standard HTTP Flash messages
        if status_choice == 'won':
            messages.success(request, f"Incredible job! Deal for {deal.lead.company} marked as WON! 🎉")
        elif status_choice == 'lost':
            messages.warning(request, f"Deal for {deal.lead.company} marked as lost.")
        else:
            messages.info(request, f"Deal pipeline successfully reopened.")
            
        return redirect('deal_profile', deal_id=deal.id)
        
    # Fallback safety redirect if status_choice is completely invalid
    messages.error(request, "Invalid status choice action.")
    return redirect('deals_dashboard')


@login_required
def delete_deal(request, deal_id):
    # 1. Fetch the deal safely (ensures the current user owns it)
    deal = get_object_or_404(Deal, id=deal_id, owner=request.user)
    
    if request.method == "POST":
        company_name = deal.lead.company if deal.lead else "Associated Lead"
        
        # 2. Delete the record
        deal.delete()
        
        # 3. Notify the user and redirect
        messages.success(request, f"Deal for {company_name} was successfully deleted.")
        return redirect('deals_dashboard')
        
    return redirect('deal_profile', deal_id=deal.id)


@login_required
def add_task(request, deal_id):
  
    deal = get_object_or_404(Deal, id=deal_id, owner=request.user)
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.deal = deal  
            task.owner = request.user

            if not task.due_date and 'due_date' in request.POST:
                task.due_date = request.POST.get('due_date')
            task.lead = deal.lead 

            task.save()
            
            messages.success(request, f'Task "{task.title}" added successfully! 🎉')

            # FIXED: Redirect straight back to the task tab page upon success!
            return redirect('tasks_dashboard')
            
        deal_tasks = Task.objects.filter(deal=deal).order_by('-created_at')
        context = {
            'deal': deal,
            'form': form, # This contains your input error messages
            'pending_tasks': deal_tasks.filter(is_completed=False),
            'completed_tasks': deal_tasks.filter(is_completed=True),
        }

        return render(request, 'smartcrm/task_detail.html', context)
    
    return redirect('tasks_dashboard')

@login_required
def delete_task(request, task_id):
    """Deletes a task securely and drops a flash message notification."""
    # Ensure the task exists and belongs strictly to the logged-in session user
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task_title = task.title
    task.delete()
    
    # Send a warning/danger notification confirming destruction
    messages.error(request, f'Task "{task_title}" was permanently deleted.')
    
    # Send them back to wherever they clicked the delete button from
    return redirect(request.META.get('HTTP_REFERER', 'tasks_dashboard'))

@login_required
def task_profile(request, deal_id):
    """Dedicated dashboard profile for tracking tasks assigned to a specific deal."""
    deal = get_object_or_404(Deal, id=deal_id, owner=request.user)
    deal_tasks = Task.objects.filter(deal=deal, owner=request.user).order_by('-created_at')
    
    context = {
        'deal': deal,
        'form': TaskForm(), 
        'pending_tasks': deal_tasks.filter(is_completed=False),
        'completed_tasks': deal_tasks.filter(is_completed=True),
    }
    return render(request, 'smartcrm/task_detail.html', context)

@login_required
def tasks_dashboard(request):
    """A central hub showing all tasks for the logged-in user across all deals."""
    # 1. Fetch all deals belonging to the user
    user_deals = Deal.objects.filter(owner=request.user).select_related('lead')
    
    # 2. Build grouped structures for the template
    deals_with_pending = []
    deals_with_completed = []
    
    total_pending_count = 0
    total_completed_count = 0

    for deal in user_deals:
        # Fetch related tasks for this specific deal
        all_deal_tasks = Task.objects.filter(deal=deal, owner=request.user).order_by('-created_at')
        
        pending_tasks = all_deal_tasks.filter(is_completed=False)
        completed_tasks = all_deal_tasks.filter(is_completed=True)
        
        # Track total counters for the master tab headers
        total_pending_count += pending_tasks.count()
        total_completed_count += completed_tasks.count()
        
        # Only include the deal in the list if it has tasks in that category
        if pending_tasks.exists():
            deals_with_pending.append({
                'deal': deal,
                'tasks': pending_tasks
            })
            
        if completed_tasks.exists():
            deals_with_completed.append({
                'deal': deal,
                'tasks': completed_tasks
            })

    context = {
        'active_page': 'tasks',
        'deals_with_pending': deals_with_pending,
        'deals_with_completed': deals_with_completed,
        'total_pending_count': total_pending_count,
        'total_completed_count': total_completed_count,
    }
    return render(request, 'smartcrm/tasks_dashboard.html', context)

@login_required
def toggle_task_status(request, task_id):
    """Switches a task between completed and pending states, then redirects back to the previous page."""
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    # Flip the boolean state flag safely
    task.is_completed = not task.is_completed
    task.save()

    # Smart redirect: sends the user back to whatever page they clicked it from
    return redirect(request.META.get('HTTP_REFERER', 'tasks_dashboard'))





