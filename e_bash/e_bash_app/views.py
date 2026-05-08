from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, EmailCode
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings
import random
import threading

def index(request):
    try:
        context = { 'first_name' : request.user.first_name }
        return render(request, 'index.html', context)         
    except AttributeError as e:
        return render(request, 'index.html')

def auth(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            # Если пользователь есть
            return JsonResponse({ 'status' : 'success' }) 
        else:
            # Если пользователя нету
            return JsonResponse({ 'status' : 'error' })      
    return render(request, 'auth.html')

def send_email_code_async(email, code):
    send_mail(
        'Продукты 24/7: код подтверждения',
        f'Ваш код подтверждения: {code}',
        'edsuyargulov@yandex.ru',
        [email],
        fail_silently=False,
    )

def reg(request):
    # Если приходит POST-запрос
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = email

        # Создаем пользователя
        user = User.objects.create_user(
            username = email, 
            email = email, 
            password = password, 
            first_name = first_name, 
            last_name = last_name,
            is_active = False
        )

        UserProfile.objects.create(
            user = user, 
        )

        code = str(random.randint(100000, 999999))

        EmailCode.objects.create(
            user = user,
            code = code
        )
        threading.Thread(
            target=send_email_code_async,
            args=(email, code)
        ).start()        

        request.session['pending_user_id'] = user.id
        return JsonResponse({
            'status': 'success',
            'redirect': '/confirm/'
        })

        login(request, user)

        return JsonResponse({'status' : 'success'})
        
    return render(request, 'reg.html')
    
def logout_view(request):
    logout(request)
    return redirect('index')

def items_list(request, clothing_type):
    clothing_type_name = ''

    if clothing_type == 'all':
        item = Item.objects.all()
        clothing_type_name = 'Всё'
    else:
        item = Item.objects.filter(clothing_type = clothing_type)

        clothing_types = Item.clothing_types
    
        for ft in clothing_types:
            if ft[0] == clothing_type:
                clothing_type_name = ft[1]
                break
            
    context = {
        'items_list' : item,
        'clothing_type' : clothing_type_name
    }
    return render(request, 'items_list.html', context)

# def items_list(request, clothing_type):
#     if clothing_type == 'all':
#         items = Item.objects.all()
#     else:
#         items =Item.objects.filter(clothing_type = clothing_type)
#     context ={
#         'items_list' : items,
#     }
#     return render(request, 'items_list.html', context)  

def item_template(request, id):
    item = Item.objects.get(id = id) # конструктор класса
    context = { 
        'item' : item
    }
    return render(request, 'item_template.html', context)

def account(request):
    print(request.user.id)
    context = {
    'username': request.user.username,
    'first_name': request.user.first_name,
    'last_name': request.user.last_name,
    'email': request.user.email,
    }
    return render(request, 'account.html', context,)

def confirm(request):
    if request.method == 'POST':
        code = request.POST.get('email-code')
        user_id = request.session.get('pending_user_id')

        if user_id:
            try:
                user = User.objects.get(id = user_id)
                email_code = EmailCode.objects.get(user = user, code = code)

                if email_code.code == code:
                    if not email_code.is_expired():
                        user.is_active = True
                        user.save()
                        email_code.delete()
                        login(request, user)
                        return JsonResponse({'status' : 'success', 'redirect' : '/account/'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Срок действия кода истек'}, status=400)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Неверный код'}, status=400)

    return render(request, 'confirm.html')
