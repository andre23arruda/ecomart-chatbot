import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils.helpers import load_file, save_file, process_response


@login_required(redirect_field_name='next', login_url='/login')
@require_http_methods(['GET'])
def home(request):
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(['POST'])
def chat(request):
    user = request.user
    prompt = request.POST.get('prompt', '')
    response = StreamingHttpResponse(process_response(prompt, user.chat))
    response['Content-Type'] = 'text/event-stream'
    return response


@require_http_methods(['GET'])
def clear_history(request):
    user = request.user
    chat = user.chat
    chat.update('')
    return JsonResponse({'ok': 'ok'})


@require_http_methods(['GET', 'POST'])
def user_login(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


@require_http_methods(['GET'])
def user_logout(request):
    logout(request)
    return redirect('login')