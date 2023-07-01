from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
import openai
from .models import Chat


# Create your views here.

OPENAI_KEY = ""
openai.api_key = OPENAI_KEY


def ask_openai(message):
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
            )
    answer = response.choices[0].text.strip()
    return answer


def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == "POST":
        message = request.POST.get('message')
        #response = ask_openai(message)
        response = "exceded"
        chat = Chat(user=request.user, message=message, response=response)
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, 'chatbot.html', {
        'chats': chats,
        })


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is None:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {
                'error_message': error_message,
                })
        auth.login(request, user)
        return redirect('chatbot')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not password1 == password2:
            error_message = "Passwords do not match."
            return render(request, 'register.html', {
                'error_message': error_message,
                })
        try:
            user = User.objects.create_user(username, email, password1)
            user.save()
            auth.login(request, user)
            return redirect('chatbot')
        except Exception as e:
            print(e)
            error_message = "Error creating account."
            return render(request, 'register.html', {
                'error_message': error_message,
                })
    return render(request, 'register.html')
