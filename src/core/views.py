import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.contrib.auth.models import User
from .models import Restaurant,Category,Dish,OrderItem,Order
from .utils.validation import validate_required_fields
from .forms.order_form import OrderForm,OrderItemForm,OrderStatusForm,OrderUpdateForm
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
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Authentication required'},
            status=401
        )
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
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Authentication required'},
            status=401
        )
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
    


#---------------------------order------------------------------------------

@csrf_exempt
@require_http_methods(["POST"])

def create_order(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Authentication required'},
            status=401
        )
    try:
        data = json.loads(request.body)
        items_data = data.get('items', [])

        if not items_data:
            return JsonResponse(
                {'error': 'At least one item is required'},
                status=400
            )

        form = OrderForm(data)
        if not form.is_valid():
            return JsonResponse(
                {'errors': form.errors},
                status=400
            )

        validated_items = []
        for item in items_data:
            item_form = OrderItemForm(item)
            if not item_form.is_valid():
                return JsonResponse(
                    {'errors': item_form.errors},
                    status=400
                )
            validated_items.append(item_form.cleaned_data)

        customer = User.objects.get(pk=form.cleaned_data['customer_id'])
        restaurant = Restaurant.objects.get(pk=form.cleaned_data['restaurant_id'])

        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                resturent=restaurant,
                 delivery_address=form.cleaned_data['delivery_address'],
                phone=form.cleaned_data['phone'],
                total_amount=data['total_amount']
            )

            for item in validated_items:
                dish = Dish.objects.get(pk=item['dish_id'])

                OrderItem.objects.create(
                    order=order,
                    dish=dish,
                    price=item['price'],
                    quantity=item['quantity']
                )

        return JsonResponse(
            {
                'message': 'Order created successfully',
                'order_id': order.id
            },
            status=201
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=400
        )
    



@csrf_exempt
@require_http_methods(["PATCH"])
def change_order_status(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Authentication required'},
            status=401
        )
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    order_id = data.get('id')
    if not order_id:
        return JsonResponse({'error': 'Order ID is required'}, status=400)
    

    status_value = data.get('status')
    if not status_value:
        return JsonResponse({'error': 'Status is required'}, status=400)

    if status_value == 'cancelled':
        msg_value = data.get('msg')
        if not  msg_value:
            return JsonResponse({'error': "'msg' is required when status is cancelled"}, status=400)

    form = OrderStatusForm({'status': status_value})
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    try:
        order = Order.objects.get(pk=order_id)
        if request.user != order.customer :
           return JsonResponse(
                {'status': 'error', 'message': 'Permission denied'},
                status=403
            )
        order.status = status_value
        order.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Order status updated',
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)




@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def manage_order(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Authentication required'},
            status=401
        )
    if request.user.id != pk :
           return JsonResponse(
                {'status': 'error', 'message': 'Permission denied'},
                status=403
            )
    try:
        order = Order.objects.prefetch_related("orderitem_set").get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if request.method == "DELETE":
        if order.status != 'pending':  
            return JsonResponse({'error': 'Cannot delete order with this status'}, status=400)
        order.delete()
        return JsonResponse({'message': 'Order deleted successfully'})

    elif request.method == "GET":
        items = [
            {
                'id': item.id,
                'dish_id': item.dish_id,
                'quantity': item.quantity,
                'price': item.price
            }
            for item in order.orderitem_set.all()
        ]
        data = {
            'id': order.id,
            'status': order.status,
            'delivery_address': order.delivery_address,
            'phone': order.phone,
            'items': items
        }
        return JsonResponse(data, status=200)

    elif request.method == "PUT":
        if order.status != 'pending':  
            return JsonResponse({'error': 'Cannot update order with this status'}, status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        form = OrderUpdateForm(data, instance=order)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Order updated successfully'}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
        




#------------------resturent order--------------------------------
@csrf_exempt
@require_http_methods(["GET"])
def get_restaurant_orders(request,pk):
    try:
        restaurant = Restaurant.objects.prefetch_related(
            'order_set__orderitem_set'
        ).get(pk=pk)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)
    orders = restaurant.order_set.all()
    order_list = []
    for order in orders:
        order_list.append({
            'id': order.id,
            'status': order.status,
            'delivery_address': order.delivery_address,
            'created_at': order.created_at,
            'phone': order.phone,
        })

    data = {
        'restaurant_id': restaurant.id,
        'restaurant_name': restaurant.name,
        'order_count': orders.count(),
        'orders': order_list
    }
    return JsonResponse(data, status=200)
















   


  