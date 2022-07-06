from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.authtoken.models import Token


# Create your views here.

class GetStatusView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({
            "status": 200,
            "message": "yes! django is working!"
        })


class RegistrationView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializers(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['message'] = "Successfully registered"
            data['name'] = account.name
            data['email'] = account.email
            data['username'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token

        else:
            data = {
                "status": 400,
                "message": "something went wrong",
                "data": serializer.errors
            }

        return Response(data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_user(request):
    user = Account.objects.get(username=request.user)
    serializer = RegistrationSerializers(user, many=False)

    return Response({
        "name": serializer.data['name'],
        "email": serializer.data['email'],
        "username": serializer.data['username']
    })


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_other_user(request, pk):
    user = Account.objects.get(username=pk)
    serializer = RegistrationSerializers(user, many=False)

    post = Post.objects.filter(user=pk)

    print(post)
    return Response({
        "name": serializer.data['name'],
        "email": serializer.data['email'],
        "username": serializer.data['username'],
        "total_post": post.count()
    })


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializers(categories, many=True)
    return Response({
        "total_categories": Category.objects.count(),
        "categories": serializer.data
    })


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def post_blog(request):
    serializer = PostSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {
            "message": "post added successfully",
            "data": serializer.data
        }
    else:
        data = {
            "message": 400,
            "errors": serializer.errors
        }

    return Response(data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_blog(request):
    posts = Post.objects.all()
    serializer = PostSerializers(posts, many=True)
    return Response(
        {
            "total_post": Post.objects.count(),
            "all_posts": serializer.data
        }
    )

@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_blog(request, pk):
    post = Post.objects.get(id=pk)
    print(post)
    serializer = PostSerializers(post, data=request.data)
    if serializer.is_valid():
        message = 'Updated successfully!'
        serializer.save()
    else:
        message = serializer.errors
    return Response({
        message
    })

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_single_blog(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializers(post, many=False)
    return Response(
        {
            "post": serializer.data
        }
    )


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_post(request, pk):
    try:
        post = Post.objects.get(id=pk, user=request.user)
        post.delete()
        return Response(
            {
                "message": "Post deleted!"
            }
        )

    except:
        return Response({
            "message": "You can't delete other's post!"
        })


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_user_blog(request):
    post = Post.objects.filter(user=request.user)
    serializer = PostSerializers(post, many=True)
    return Response({
        "total_posts": post.count(),
        "post": serializer.data
    })


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_post_by_category(request, pk):
    posts = Post.objects.filter(category_id=pk)
    serializer = PostSerializers(posts, many=True)
    return Response(
        {
            "total_post": posts.count(),
            "all_posts": serializer.data
        }
    )


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def post_comment(request):
    serializer = CommentSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {
            "message": "Comment added successfully!",
            "comment": serializer.data
        }

    else:
        data = {
            "message": "Something went wrong!"
        }

    return Response(data)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_comment(request, pk):
    comment = Comment.objects.filter(post_id=pk)
    serializer = CommentSerializers(comment, many=True)
    return Response({
        "total_comment": comment.count(),
        "comment": serializer.data
    })


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(id=pk, user_id=request.user)
        comment.delete()
        return Response({
            "message": "Comment deleted!"
        })
    except:
        return Response({
            "message": "You can't delete other's comment!"
        })
