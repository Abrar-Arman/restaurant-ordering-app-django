import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Restaurant,Category,Dish
from .utils.validation import validate_required_fields
@csrf_exempt
@require_http_methods(["GET", "POST"])
def restaurants(request):
    if request.method == "GET":
        restaurants = list(Restaurant.objects.values('id', 'name', 'email', 'phone', 'created_at'))    
        return JsonResponse({
            'status': 'success',
            'data': restaurants
        }, safe=False)
    
    if request.method=="POST":
        data=json.loads(request.body)
        is_valid, missing= validate_required_fields(data,['name', 'email', 'phone'])
        if not is_valid:
            return JsonResponse({
                'msg': f'Missing required fields: {", ".join(missing)}'
            },status=400)
        restaurant = Restaurant.objects.create(name=data['name'],email=data['email'],phone=data['phone'] )
        return JsonResponse({
            "msg":'Restaurant created successfully',
            "status":'success',
            "id":restaurant.id
        },status=201)
    

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def restaurant_detail(request, pk):
    if request.method == "GET":
        try:
            restaurant = Restaurant.objects.prefetch_related('dish_set', 'ratings').get(pk=pk)   
            
            dishes = []
            for dish in restaurant.dish_set.all():  
                dishes.append({
                    "id": dish.id,
                    "name": dish.name,
                    "price": dish.price,
                    "description": dish.description,
                    "thumbnail": (
                        request.build_absolute_uri(dish.thumbnail.url)
                        if dish.thumbnail else None
                    ),
                    "is_avalible":dish.is_avalible
                })        
            ratings = restaurant.ratings.select_related('user_set').filter(type='resturent').values('id', 'score', 'comment', 'created_at', 'user__username')
            
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': restaurant.id,
                    'name': restaurant.name,
                    'email': restaurant.email,
                    'phone': restaurant.phone,
                    'created_at': str(restaurant.created_at),
                    'dishes': dishes,
                    'ratings': list(ratings)
                }
            })
        except Restaurant.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Restaurant not found'
            }, status=404)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            is_valid, missing= validate_required_fields(data,['name', 'email', 'phone'])
            if not is_valid:
                return JsonResponse({
                    'msg': f'Missing required fields: {", ".join(missing)}'
                },status=400)
            
            restaurant = Restaurant.objects.get(pk=pk)
            restaurant.name = data['name']
            restaurant.email = data['email']
            restaurant.phone = data['phone']
            restaurant.save()            
            return JsonResponse({
                'status': 'success',
                'message': 'Restaurant updated successfully',
                'id': restaurant.id,
                
            })
        except Restaurant.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Restaurant not found'
            }, status=404)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    elif request.method == "DELETE":
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            restaurant_name = restaurant.name
            restaurant.delete()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Restaurant {restaurant_name} deleted successfully'
            })
        except Restaurant.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Restaurant not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        


#dish end point 
@csrf_exempt
@require_http_methods(["POST"])
def create_dish(request):
    content_type = request.META.get('CONTENT_TYPE', '')
    if 'multipart/form-data' not in content_type:
        return JsonResponse(
            {'error': 'Content-Type must be multipart/form-data'},
            status=400
        )

    data = request.POST
    files = request.FILES

    is_valid, missing = validate_required_fields(
        data,
        ['name', 'description', 'price', 'restaurant_id', 'category_id']
    )
    if not is_valid:
        return JsonResponse(
            {"msg": f"Missing required fields: {', '.join(missing)}"},
            status=400
        )

   
    try:
        restaurant = Restaurant.objects.get(pk=data.get('restaurant_id'))
    except Restaurant.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Restaurant not found'},
            status=400
        )

    
    try:
        category = Category.objects.get(pk=data.get('category_id'))
    except Category.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Category not found'},
            status=400
        )

    thumbnail = files.get('thumbnail')

    dish = Dish.objects.create(
        name=data.get('name'),
        description=data.get('description'),
        price=data.get('price'),
        restaurant=restaurant,   
        Category=category,      
        thumbnail=thumbnail
    )

    return JsonResponse(
        {
            'message': 'Dish created successfully',
            'id': dish.id
        },
        status=201
    )



@csrf_exempt
@require_http_methods(["DELETE","PUT"])
def dish_operation(request,pk):
    if request.method=="DELETE":
        try:
            dish=Dish.objects.get(pk=pk)
            dish_name=dish.name
            dish.delete()
            return JsonResponse({
                'status': 'success',
                'message': f'Dish {dish_name} deleted successfully'
            })
        except Dish.DoesNotExist:
             return JsonResponse({
                'status': 'error',
                'message': 'Dish not found'
            }, status=404)
        
   

@csrf_exempt
@require_http_methods(["PATCH"])
def set_availability(request):
    try:
      data = json.loads(request.body)
      is_valid, missing = validate_required_fields(
        data,
        ['id','is_avalible' ])
      if not is_valid:
           return JsonResponse(
            {"msg": f"Missing required fields: {', '.join(missing)}"},
            status=400
        )
          
      try:
        dish = Dish.objects.get(pk=data['id'])
        dish.is_avalible = data['is_avalible']
        dish.save()
        return JsonResponse({
            'success': True,
            'message': 'Availability updated successfully',
            'id': dish.id,
        }, status=200)
    
      except Dish.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dish not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
   








              
           
          
    

    

        


    

