import json
from django.http import JsonResponse
from django.views import View
from blog_app.models import Post, Comment, Category
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from pprint import pprint
from django.db import connection

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class PostListCreateView(View):
    def serialize_post(self, post):
        return {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.isoformat(),
            'category': {
                'id': post.category.id,
                'name': post.category.name
            } if post.category else None,
            'comments': [
                {
                    'id': comment.id,
                    'content': comment.content,

                } for comment in post.comments.all()
            ]
        }

    # This is the simplier way implementation of get PostListCreateView, but it is less efficient 
    # because it will make an extra query to get the category and then another query to get the comments related 
    # to that post. The implementation below is more efficient because it uses select_related and prefetch_related 
    # to fetch the related category and comments in a single query.

    # def get(self, request):
    #     posts = Post.objects.all()
    #     data = [self.serialize_post(post) for post in posts]
    #     pprint(connection.queries)
    #     return JsonResponse(data, safe=False)

    def get(self, request):
        posts = Post.objects.select_related('category').prefetch_related('comments').all()
        data = [self.serialize_post(post) for post in posts]
        pprint(connection.queries)
        return JsonResponse(data, safe=False)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            title = data.get('title')
            content = data.get('content')
            category_id = data.get('category_id')
            if not title or not content:
                return JsonResponse({'error': 'Title and content are required.'}, status=400)
            post = Post.objects.create(title=title, content=content, category_id=category_id)
            return JsonResponse(self.serialize_post(post), status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class PostDetailView(View):
    def serialize_post(self, post):
        return {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.isoformat(),
            'category': post.category.name if post.category else None,
        }

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            return JsonResponse(self.serialize_post(post))
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found.'}, status=404)
        
        
    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            data = json.loads(request.body)
            post.title = data.get('title', post.title)
            post.content = data.get('content', post.content)
            category_id = data.get('category_id')
            if category_id is not None:
                post.category_id = category_id
            post.save()
            pprint(connection.queries) 
            return JsonResponse(self.serialize_post(post))
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return JsonResponse({'message': 'Post deleted successfully.'})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found.'}, status=404)
    
@method_decorator(csrf_exempt, name='dispatch')
class CommentListCreateView(View):
    def serialize_comment(self, comment):
        return {
            'id': comment.id,
            'post': {
                'id': comment.post.id,
                'title': comment.post.title,
                'content': comment.post.content
            },
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
        }

    def get(self, request, post_pk):
        try:
            if not Post.objects.filter(pk=post_pk).exists():
                return JsonResponse({'error': 'Post not found.'}, status=404)
            comments = Comment.objects.select_related('post').filter(post_id=post_pk)
            data = [self.serialize_comment(comment) for comment in comments]
            pprint(connection.queries)
            return JsonResponse(data, safe=False)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found.'}, status=404)
    
    def post(self, request, post_pk):
        try:
            if not Post.objects.filter(pk=post_pk).exists():
                return JsonResponse({'error': 'Post not found.'}, status=404)
            data = json.loads(request.body)
            content = data.get('content')
            if not content:
                return JsonResponse({'error': 'Content is required.'}, status=400)
            comment = Comment.objects.create(post_id=post_pk, content=content)
            return JsonResponse(self.serialize_comment(comment), status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        
        
class PostListByCategoryView(View):
    def serialize_post(self, post):
        return {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.isoformat(),
            'category': post.category.name if post.category else None,
        }

    def get(self, request, category_id):
        if not Category.objects.filter(id=category_id).exists():
            return JsonResponse({'error': 'Category not found.'}, status=404)
        posts = Post.objects.select_related('category').filter(category_id=category_id)
        if not posts.exists():
            return JsonResponse({'error': 'No posts found for this category.'}, status=404)
        data = [self.serialize_post(post) for post in posts]
        pprint(connection.queries)
        return JsonResponse(data, safe=False)
    

    # other way to implement get method for PostListByCategoryView but less efficient because 
    # it will make an extra query to get the category and then another query to get the posts related to that category. 
    # The above implementation is more efficient because it directly filters the posts based on the category_id without 
    # needing to fetch the category first.
    
    # def get(self, request, category_id):
    #     category = Category.objects.filter(id=category_id).first()
    #     print(category)
    #     if not category:
    #         return JsonResponse({'error': 'Category not found.'}, status=404)
        
    #     posts = category.posts.all()
    #     data = [self.serialize_post(post) for post in posts]
    #     return JsonResponse(data, safe=False)