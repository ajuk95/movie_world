from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse


def logout(request):
    auth.logout(request)
    print("user logged out")
    return redirect('/movies')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print(user, "user logged in")
            return redirect("/movies")
        else:
            print("invalid user credentials")
            messages.info(request, "invalid credentials")
            return redirect(reverse("credentials:login"))
    return render(request, 'login.html')

def register(request):
    # return HttpResponse("hi")
    if request.method == "POST":
        try:
            username = request.POST['username']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']
            password1 = request.POST['password1']
            if username and email and password and password1 and password == password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "username already exists")
                    return redirect(reverse("credentials:register"))
                elif User.objects.filter(email=email).exists():
                    messages.info(request, "email already exists")
                    return redirect(reverse("credentials:register"))
                else:
                    user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname, email=email)
                    user.save()
                    print("user registered:", user)

                    # send a welcome message to the registered email
                    send_welcome_email(email, username)
                    print("welcome message sent to", email)

                    return redirect(reverse("credentials:login"))
            else:
                messages.info(request, "invalid credentials")
                return redirect(reverse("credentials:register"))
        except:
            messages.info(request, "invalid credentials")
    return render(request, "register.html")


def send_welcome_email(user_email, username):
    subject = 'Welcome to Our Site!'
    html_message = render_to_string('welcome_email.html', {'username': username})
    plain_message = "Thank you for registering on our website. We're excited to have you as a member of our community."
    from_email = 'your-email@example.com'
    to = [user_email]
    send_mail(subject, plain_message, from_email, to, html_message=html_message)


