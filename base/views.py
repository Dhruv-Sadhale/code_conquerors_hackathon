from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from .models import Club_Primary
from .models import QuizResponse, ClubResponse, UserEmail
from django import forms
from .models import Question  # Import the Question model
from django.contrib.auth.decorators import login_required
from .forms import UserFeedbackForm
from .models import UserFeedback
import random
from django.core.mail import send_mail
# views.py
from django.shortcuts import render, redirect
from .models import Notification
from .forms import NotificationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import QuizResponse

# views.py
from django.utils import timezone
import qrcode
from django.shortcuts import render, redirect
from django.http import HttpResponse
from io import BytesIO
from .models import Club_Primary, Club_Secondary,Attendance
from django.contrib.auth.decorators import login_required


def explore(request, pk):
     club_object = get_object_or_404(Club_Primary, club=pk)
     print(club_object)
     club_responses = ClubResponse.objects.filter(club=club_object)
     recommended_users = [response.user.username for response in club_responses]
     print(recommended_users)
     return render(request, 'base/explore.html', {'club_object': club_object, 'recommended_users': recommended_users})
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json

def core(request, pk):
    # Retrieve the club object based on the primary key (pk)
    club_object = get_object_or_404(Club_Secondary, club=pk)
        
    # Retrieve all inducted members for the club
    inducted_members = club_object.inductees.all()

    # Check if the currently logged-in user is in the list of inductees
    current_user = request.user
    # if current_user not in inducted_members:
    #     # If the user is not in the list of inductees, return an HTTP response with an alert message
    #     alert_message = json.dumps({'message': 'You are not an inducted member of this club.'})
    #     return HttpResponse(alert_message, content_type='application/json')
    # else:
        # If the user is in the list of inductees, render the core.html template
    return render(request, 'base/core.html', {'club_object': club_object, 'inducted_members': inducted_members})


@login_required(login_url='login')  # Adjust login URL
def generate_qrcode(request, club_name):
    club = Club_Primary.objects.get(club=club_name)
    qr_code_data = club.generate_qrcode_data()

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data(qr_code_data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Create a BytesIO buffer to store the image
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the image as an HTTP response
    return HttpResponse(buffer.read(), content_type="image/png")

@login_required(login_url='login')  # Adjust login URL
def attend_club(request,club_name):
    user = request.user
    club = Club_Primary.objects.get(club=club_name)

    # Check if the user has already attended
    if not Attendance.objects.filter(user=user, club=club).exists():
        # Record attendance
        Attendance.objects.create(user=user, club=club)

    # Redirect to the explore/club page
    return HttpResponse(f'Attendance recorded for {request.user} in {club_name}')






def home(request): 
   
    return render(request, 'base/home.html')
def clubs(request):
    notifications = Notification.objects.all().order_by('-timestamp')[:10]
    if(notifications):
        print(notifications)
    else:
        print("NOT WORKING!!!!")
    return render(request, 'base/clubs.html', {'notifications': notifications})
    
def submit_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.club = request.user.club  # Assuming clubs are associated with users
            notification.save()
            return redirect('clubs')
    else:
        form = NotificationForm()
    return render(request, 'base/submit_notification.html', {'form': form})




def send_email_notification(user, recommended_clubs):
    subject = 'Club Recommendation Notification'
    message = f"Hello {user.username},\n\n" \
              f"We have received your club recommendations. The recommended clubs are: {', '.join(recommended_clubs)}.\n" \
              f"Thank you for using our platform!\n\n" \
              f"Best regards,\nThe Club Navigator Team"

    from_email = 'your_email@example.com'  # Replace with your email
    to_email = [user.email]  # Use the user's email

    send_mail(subject, message, from_email, to_email)




@login_required(login_url='login')
def dashboard(request):
    # Retrieve the user's ID from the session
    user_id = request.session.get('user_id')

    # Check if user_id is present in the session
    if user_id is not None:
        # Fetch the user's responses to display on the dashboard
        user_responses = ClubResponse.objects.filter(user_id=user_id)

        # Fetch the clubs in which the user is an inductee
        inducted_clubs = Club_Secondary.objects.filter(inductees=request.user)
        
        # Pass user_responses and inducted_clubs to the template
        return render(request, 'base/dashboard.html', {'user_responses': user_responses, 'username': request.user.username, 'inducted_clubs': inducted_clubs})
    else:
        # Redirect to the login page if user_id is not present
        return redirect('login')

@login_required(login_url='login')  # Use the appropriate URL for your login view

def questionnaire(request):
    return render(request, 'base/index.html')
from django.db.models import F
@csrf_exempt
@login_required(login_url='login')
def record_club(request):
    if request.method == 'POST':
        try:
            data_list = json.loads(request.body)
            print('Received data:', data_list)
            club = data_list['club']
            
            print(club)
            
            # Validate the data structure
            # if not isinstance(data_list, list):
            #     raise ValueError("Invalid data structure")

            responses = []
            # ClubResponse.objects.filter(user=request.user).delete()
            user_responses = ClubResponse.objects.filter(user=request.user).order_by('-timestamp')
            
            # Keep only the last three responses
            if len(user_responses) > 2:
                user_responses_to_delete = list(user_responses[2:])
                ClubResponse.objects.filter(id__in=[obj.id for obj in user_responses_to_delete]).delete()
            print(responses)
            if club is not None :
                user_email, created = UserEmail.objects.get_or_create(user=request.user, defaults={'email': request.user.email})
                responses.append(
                    ClubResponse(
                        user=request.user,  # Assuming you're using Django authentication
                        club=club,
                        timestamp=timezone.now()  # Assuming you have a timestamp field in ClubResponse                        
                    )
                )

            # Use bulk_create for better performance
            ClubResponse.objects.bulk_create(responses)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print('Error processing responses:', str(e))
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
@login_required(login_url='login')  # Use the appropriate URL for your login view
def record_response(request):
    if request.method == 'POST':
        try:
            data_list = json.loads(request.body)
            print('Received data:', data_list)
            question_number = data_list['question_number']
            selected_option = data_list['selected_option']
            print(question_number)
            print(selected_option)
            # Validate the data structure
            # if not isinstance(data_list, list):
            #     raise ValueError("Invalid data structure")

            responses = []
            
             
            if question_number is not None and selected_option is not None:
                responses.append(
                    QuizResponse(
                        user=request.user,  # Assuming you're using Django authentication
                        question_number=question_number,
                        selected_option=selected_option,
                    )
                )

            # Use bulk_create for better performance
            QuizResponse.objects.bulk_create(responses)

           

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print('Error processing responses:', str(e))
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method =='POST':
        username  = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user= User.objects.get(username= username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')
        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)
            # return render(request, 'base/dashboard.html')
            request.session['user_id'] = user.id
            return redirect('dashboard')
        else:
            messages.error(request, "username or password does not exist")
    context= {'page':page}
    return render(request , 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
        
        # page='register'
        form= UserCreationForm()
        if request.method =='POST':
            form= UserCreationForm(request.POST)
            if form.is_valid():
                user= form.save(commit=False)
                user.username=user.username.lower()
                user.save()
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "an error occured during registration")
        return render(request, 'base/login_register.html', {'form':form})



def satisfaction(request):
    satisfied = request.GET.get('satisfied', '')

    if satisfied.lower() == 'no':
        # User is not satisfied, present feedback form
        if request.method == 'POST':
            feedback_form = UserFeedbackForm(request.POST)
            if feedback_form.is_valid():
                # Save user feedback
                feedback = feedback_form.save(commit=False)
                feedback.user = request.user
                feedback.save()
                return redirect('questionnaire')  
        else:
            feedback_form = UserFeedbackForm()

        return render(request, 'base/feedback_form.html', {'feedback_form': feedback_form})
    else:
        # User is satisfied, redirect to the questionnaire or any other page
        # return redirect('dashboard')  # Adjust the URL as needed
        return redirect('display_recommendations')
    
def induction(request):
    username = request.user.username
    user_id = request.session.get('user_id')

    # Check if user_id is present in the session
    if user_id is not None:
        # Fetch the user's responses to display on the dashboard
        user_responses = ClubResponse.objects.filter(user_id=user_id)
        inducted_clubs = Club_Secondary.objects.filter(inductees=request.user)
        club_names = [club.club for club in inducted_clubs]
        print("next line shows inducted clubs:")
        print(inducted_clubs)
        inducted_clubs_js = [club.club for club in Club_Secondary.objects.filter(inductees=request.user)]

    # Convert the list to JSON string
        inducted_clubs_json = json.dumps(inducted_clubs_js)
        # Pass user_responses to the template
        return render(request, 'base/induction.html', {'user_responses': user_responses, 'username': username, 'inducted_clubs': club_names, 'inducted_club_js':inducted_clubs_json})
    else:
        # Redirect to the login page if user_id is not present
        return redirect('login')



def record_applicant(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            club_name = data['clubName']
            user_id = data['userId']
            print(club_name)
            print(user_id)
            # Get or create the Club_Secondary object
            club, created = Club_Secondary.objects.get_or_create(club=club_name)
            
            # Get the current user based on user_id
            user = User.objects.get(pk=user_id)
            print(user)
            # Add the current user to the applicants field
            print(club.applicants)

            club.applicants.add(user)
            print(club.applicants)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print('Error recording applicant:', str(e))
            return JsonResponse({'status': 'error', 'message': 'An error occurred'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# views.py

from django.shortcuts import redirect, get_object_or_404
from .models import Club_Secondary, User

from django.shortcuts import redirect

def transfer_applicants(request, club_name):
    if request.method == 'POST':
        # Retrieve selected applicants from the form submission
        selected_applicants = request.POST.getlist('selected_applicants')
        print(selected_applicants)
        # Get the Club_Secondary object
        club = Club_Secondary.objects.get(club=club_name)

        # Move selected applicants from applicants to inductees
        for applicant_id in selected_applicants:
            integer_value=int(applicant_id.strip('[]"'))
            applicant = User.objects.get(pk=integer_value)
            club.applicants.remove(applicant)
            club.inductees.add(applicant)

        # Redirect back to the same page
        return redirect('core', pk=club_name)
    else:
        # Handle GET request (if needed)
        pass
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ClubResponse

@csrf_exempt
def delete_user_response(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        
        # Extract the club name from the parsed data
        club_name = data.get('clubName')
        
        # Get the user's response for the given club
        user_response = ClubResponse.objects.filter(user=request.user, club=club_name).first()
        
        if user_response:
            # Delete the user's response
            user_response.delete()
            return JsonResponse({'message': 'User response deleted successfully'}, status=200)
        else:
            return JsonResponse({'error': 'User response not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


