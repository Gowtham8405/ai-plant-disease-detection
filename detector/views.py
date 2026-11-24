from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.conf import settings

from .forms import LeafUploadForm, UserRegisterForm, UserLoginForm
from .models import PlantLeafUpload, PredictionHistory
from .ai.predictor import predict_disease
from .ai.disease_info import get_disease_info


def home_view(request):
    """
    Homepage view for AI Plant Disease Detection.
    Handles rendering the upload interface, saving submitted leaf images,
    invoking the MobileNetV2 AI prediction service, retrieving
    disease profiles & recommendations, and automatically persisting
    results to user history when authenticated.
    """
    uploaded_image = None
    prediction_result = None
    disease_info = None

    if request.method == 'POST':
        form = LeafUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded leaf image into database & media folder
            uploaded_image = form.save()

            # Execute AI inference on the uploaded leaf image
            threshold = getattr(settings, 'PLANT_DISEASE_CONFIDENCE_THRESHOLD', 0.70)
            prediction_result = predict_disease(
                uploaded_image.image.path,
                confidence_threshold=threshold
            )

            if prediction_result.get('success'):
                predicted_class = prediction_result.get('predicted_class')
                is_confident = prediction_result.get('is_confident', False)

                # Fetch supplementary disease metadata
                disease_meta = get_disease_info(predicted_class)
                plant_name = disease_meta.get('plant_name', 'Unknown Plant')
                disease_name = disease_meta.get('disease_name', predicted_class)
                is_healthy = disease_meta.get('is_healthy', False)

                if is_confident:
                    # Retrieve disease information and recommendations only for confident predictions
                    disease_info = disease_meta
                    messages.success(
                        request,
                        f"Analysis Complete: Detected '{predicted_class}' with {prediction_result['confidence_percent']}% confidence."
                    )
                else:
                    # Low-confidence: Do not assign confirmed disease recommendations
                    disease_info = None
                    messages.warning(
                        request,
                        prediction_result.get('status_message', 'Prediction confidence is below threshold.')
                    )

                # Save to user prediction history if authenticated
                if request.user.is_authenticated:
                    PredictionHistory.objects.create(
                        user=request.user,
                        image=uploaded_image.image,
                        plant_name=plant_name,
                        disease_name=disease_name,
                        full_class_name=predicted_class,
                        confidence_percent=prediction_result.get('confidence_percent', 0.0),
                        is_confident=is_confident,
                        is_healthy=is_healthy,
                        status_message=prediction_result.get('status_message', ''),
                    )
            else:
                messages.error(
                    request,
                    prediction_result.get('error', 'Unable to process image with AI model.')
                )
        else:
            error_msg = "Please provide a valid image file (JPG, JPEG, PNG, or WEBP)."
            if form.errors and 'image' in form.errors:
                error_msg = form.errors['image'][0]
            messages.error(request, error_msg)
    else:
        form = LeafUploadForm()

    context = {
        'form': form,
        'uploaded_image': uploaded_image,
        'prediction_result': prediction_result,
        'disease_info': disease_info,
        'page_title': 'AI Plant Disease Detection',
    }
    return render(request, 'detector/home.html', context)


# ==============================================================================
# Authentication Views (Register, Login, Logout)
# ==============================================================================

def register_view(request):
    """
    User registration view with secure password hashing.
    """
    if request.user.is_authenticated:
        return redirect('detector:dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to PlantGuard AI, {user.username}! Your account was created successfully.")
            return redirect('detector:dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'detector/register.html', {
        'form': form,
        'page_title': 'Create an Account - PlantGuard AI'
    })


def login_view(request):
    """
    User login view supporting standard username/password authentication.
    """
    if request.user.is_authenticated:
        return redirect('detector:dashboard')

    next_url = request.GET.get('next', 'detector:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_page = request.POST.get('next') or 'detector:dashboard'
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'detector/login.html', {
        'form': form,
        'next': next_url,
        'page_title': 'Login - PlantGuard AI'
    })


def logout_view(request):
    """
    User logout view.
    """
    if request.user.is_authenticated:
        username = request.user.username
        auth_logout(request)
        messages.info(request, f"You have been successfully logged out, {username}.")
    return redirect('detector:home')


# ==============================================================================
# Authenticated User Dashboard & Prediction History Views
# ==============================================================================

@login_required
def dashboard_view(request):
    """
    Authenticated user overview dashboard displaying stats and recent diagnoses.
    """
    user_predictions = PredictionHistory.objects.filter(user=request.user)
    total_count = user_predictions.count()
    healthy_count = user_predictions.filter(is_healthy=True).count()
    disease_count = user_predictions.filter(is_healthy=False, is_confident=True).count()
    uncertain_count = user_predictions.filter(is_confident=False).count()
    recent_predictions = user_predictions[:5]

    context = {
        'total_count': total_count,
        'healthy_count': healthy_count,
        'disease_count': disease_count,
        'uncertain_count': uncertain_count,
        'recent_predictions': recent_predictions,
        'page_title': 'User Dashboard - PlantGuard AI',
    }
    return render(request, 'detector/dashboard.html', context)


@login_required
def history_view(request):
    """
    List view of all predictions belonging exclusively to the logged-in user.
    """
    history_queryset = PredictionHistory.objects.filter(user=request.user)

    # Optional filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'healthy':
        history_queryset = history_queryset.filter(is_healthy=True)
    elif status_filter == 'disease':
        history_queryset = history_queryset.filter(is_healthy=False, is_confident=True)
    elif status_filter == 'uncertain':
        history_queryset = history_queryset.filter(is_confident=False)

    # Optional search by plant / disease
    search_query = request.GET.get('q', '').strip()
    if search_query:
        history_queryset = history_queryset.filter(
            full_class_name__icontains=search_query
        )

    # Paginate results (10 per page)
    paginator = Paginator(history_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_history_count': PredictionHistory.objects.filter(user=request.user).count(),
        'status_filter': status_filter,
        'search_query': search_query,
        'page_title': 'Prediction History - PlantGuard AI',
    }
    return render(request, 'detector/history.html', context)


@login_required
def history_detail_view(request, id):
    """
    Detail view for an individual prediction record.
    Enforces strict user isolation: User A cannot view User B's record.
    """
    record = get_object_or_404(PredictionHistory, id=id, user=request.user)
    disease_info = get_disease_info(record.full_class_name) if record.is_confident else None

    context = {
        'record': record,
        'disease_info': disease_info,
        'page_title': f"{record.full_class_name} - Diagnosis Details",
    }
    return render(request, 'detector/history_detail.html', context)


@login_required
@require_POST
def delete_history_view(request, id):
    """
    Delete a single prediction history record.
    Strictly restricted to the record owner.
    """
    record = get_object_or_404(PredictionHistory, id=id, user=request.user)
    record_name = record.full_class_name
    record.delete()
    messages.success(request, f"Diagnosis record for '{record_name}' was deleted.")
    return redirect('detector:history')


@login_required
@require_POST
def clear_history_view(request):
    """
    Delete all prediction history records belonging ONLY to the logged-in user.
    """
    deleted_count, _ = PredictionHistory.objects.filter(user=request.user).delete()
    messages.success(request, f"Successfully cleared all {deleted_count} prediction history record(s).")
    return redirect('detector:history')


# ==============================================================================
# Informational & Profile Pages (Multi-Page Structure)
# ==============================================================================

def how_it_works_view(request):
    """
    Dedicated page explaining the 3-step AI plant disease diagnosis pipeline.
    """
    return render(request, 'detector/how_it_works.html', {
        'page_title': 'How It Works - PlantGuard AI'
    })


def about_view(request):
    """
    Dedicated About page explaining project background, technology stack,
    and 95.33% test dataset accuracy.
    """
    return render(request, 'detector/about.html', {
        'page_title': 'About This Project - PlantGuard AI'
    })


@login_required
def profile_view(request):
    """
    User profile page displaying authenticated account info and diagnosis statistics.
    """
    user_predictions = PredictionHistory.objects.filter(user=request.user)
    total_count = user_predictions.count()
    healthy_count = user_predictions.filter(is_healthy=True).count()
    disease_count = user_predictions.filter(is_healthy=False, is_confident=True).count()

    context = {
        'user': request.user,
        'total_count': total_count,
        'healthy_count': healthy_count,
        'disease_count': disease_count,
        'page_title': f"{request.user.username}'s Profile - PlantGuard AI",
    }
    return render(request, 'detector/profile.html', context)


