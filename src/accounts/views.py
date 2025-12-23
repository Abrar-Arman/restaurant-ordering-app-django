from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
import json
from .forms.signup import SignUpForm
from .forms.login import LoginForm




#--------------------------user role --------------


def user_role(request):
     if not request.user.is_authenticated:
            return JsonResponse(
                {'status': 'error', 'message': 'Authentication required'},
                status=401
            )
     user = request.user
     is_owner = user.restaurant_set.exists() 
     return JsonResponse({
        "user_id": user.id,
        "username": user.username,
        "is_owner": is_owner
    })


@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    try:
        data=json.loads(request.body)
        form = SignUpForm(data)
        if form.is_valid():
                    user = form.save()
                    login(request, user)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Account created successfully',
                        'user': {
                            'email': user.email
                        }
                    }, status=201)
        else:
                    return JsonResponse({
                        'status': 'error',
                        'errors': form.errors
                    }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    
@csrf_exempt
@require_http_methods(["POST"])
def login(request):
       try:
              data=json.loads(request.body)
              form=LoginForm(data)
              if  form.is_valid():
                  try:
                      user = User.objects.get(email=data['email'])
                      if user.check_password(data['password']):
                          auth_login(request, user)
                          return JsonResponse({
                                'status': 'success',
                                'message': 'Logged in successfully',
                                'user': {
                                    'username': user.username,
                                    'email': user.email,
                                    'first_name': user.first_name
                                }
                            }, status=200)
                      
                  except User.DoesNotExist:
                            return JsonResponse({
                                'status': 'error',
                                'message': 'Invalid email or password'
                            }, status=401)
              else:
                        return JsonResponse({
                        'status': 'error',
                        'errors': form.errors
                    }, status=401)                    
       except json.JSONDecodeError:
         return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
       


@csrf_exempt
@require_http_methods(["DELETE"])
def logout(request):
       try:
            if request.user.is_authenticated:
                auth_logout(request)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Logged out successfully'
                }, status=200)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'User is not logged in'
                }, status=401)
       except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred during logout'
            }, status=500)
      
       

