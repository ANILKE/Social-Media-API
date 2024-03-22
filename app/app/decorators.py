# from django.core.cache import cache
# from functools import wraps
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.renderers import JSONRenderer


# def custom_cache_page(timeout=60):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request, *args, **kwargs):
#             print(request.path)
#             cache_key = f"{request.path}"
#             cached_response_data = cache.get(cache_key)
#             if cached_response_data:
#                 return Response(cached_response_data)
#             response = view_func(request, *args, **kwargs)
            
#             cache.set(cache_key, response.data, timeout=timeout)
#             Res = Response(response.data)
#             Res.accepted_renderer = JSONRenderer()
#             Res.accepted_media_type = 'application/json'
#             Res.renderer_context = {}
#             return Res
#         return wrapper
#     return decorator