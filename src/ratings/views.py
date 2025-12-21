import json
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import Rating
from core.models import Restaurant,Order
from .forms.ratings_form import RestaurantRatingForm,RatingForm



# ------------------- resturent ratings -------------------
@csrf_exempt
@require_http_methods(["POST"])
def create_rating(request,pk):
   if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Authentication required'},
            status=401
        )
   try:
        restaurant = Restaurant.objects.get(pk=pk)
   except Restaurant.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Restaurant not found'},
            status=404
        )
   try:
        data = json.loads(request.body)
   except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid JSON format'},
            status=400
        )
   restaurant_rating_form = RestaurantRatingForm(data)
   if not restaurant_rating_form.is_valid():
        return JsonResponse(
            {'errors': restaurant_rating_form.errors},
            status=400
        )
   user = User.objects.get(pk=data['customer_id'])
   if not Order.objects.filter(
        customer=user,
        resturent=restaurant,
        status='confirmed'
    ).exists():
        return JsonResponse(
            {
                'status': 'error',
                'message': 'You can only rate restaurants you have ordered from'
            },
            status=403
        )

   Rating.objects.create(
        user=user,
        score=data['score'],
        comment=data.get('comment'),
        type='restaurant',
        content_type=ContentType.objects.get_for_model(Restaurant),
        object_id=restaurant.id
    )
   return JsonResponse(
        {
            'message': 'Rating created successfully'
        },
        status=201
    )


@csrf_exempt
@require_http_methods(["DELETE","PUT"])
def manage_rating(request,pk):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Authentication required'},
            status=401
        )
    try:
        rating = Rating.objects.get(pk=pk)
    except Rating.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Rating not found'},
            status=404
        )
    if rating.user != request.user:
            return JsonResponse(
                {'status': 'error', 'message': 'Permission denied'},
                status=403
            )
         
         
    if request.method=="DELETE":
          rating.delete()
          return JsonResponse({
                'status': 'success',
                'message': 'rating deleted successfully'
            })
    if request.method=="PUT":
         try:
             data=json.loads(request.body)
         except json.JSONDecodeError:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid JSON format'},
                status=400
                )
         rating_form=RatingForm(data)
         if rating_form.is_valid():
                  rating.score=data['score']
                  rating.comment=data['comment']
                  rating.save()
                  return JsonResponse({
                      'status': 'success',
                    'message': 'Rating updated successfully',
                      
                  })
         else:
                  return JsonResponse(  {'errors': rating_form.errors},status=400 )
         



# -------------------- user rating--------------------------
@csrf_exempt
@require_http_methods(["GET"])
def user_ratings(request,pk):
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
           user=User.objects.prefetch_related('rating_set').get(pk=pk)
           ratings = []
        
           for rate in user.rating_set.all():
                ratings.append({
                    'id': rate.id,
                    'score': rate.score,
                    'comment': rate.comment,
                    'created_at': rate.created_at
                })
            
           return JsonResponse({
                'user_id': user.id,
                'ratings':ratings
            }, status=200)
      
      except User.DoesNotExist:
           return JsonResponse(  {'status': 'error', 'message': 'Rating not found'},
            status=404)
      
                                  
        
