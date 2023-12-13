from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from pickleapi.models import Post, PickleUser, Court
from .users import PickleUserSerializer
from .categories import CategorySerializer
from .courts import CourtSerializer
from rest_framework import permissions

class SimplePostSerializer(serializers.ModelSerializer):

    court = CourtSerializer(many=False)
    
    class Meta:
        model = Post
        fields = [
            "title",
            "image_url",
            "content",
            "categories",
            "court",
        ]

class PostSerializer(serializers.ModelSerializer):
    pickle_user = PickleUserSerializer(many=False)
    is_owner = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)
    court = CourtSerializer(many=False)

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.pickle_user.user

    class Meta:
        model = Post
        fields = [
            "id",
            "pickle_user",
            "title",
            "publication_date",
            "image_url",
            "content",
            "court",
            "categories",
            "is_owner",
        ]

class PostViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={"request": request})
            return Response(serializer.data)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        pickle_user = PickleUser.objects.get(user=request.auth.user)
        title = request.data.get("title")
        publication_date = request.data.get("publication_date")
        image_url = request.data.get("image_url")
        content = request.data.get("content")
        court_id = request.data.get("court")
        court = None if court_id == 0 else Court.objects.get(pk=court_id)

        post = Post.objects.create(
            pickle_user=pickle_user,
            title=title,
            publication_date=publication_date,
            image_url=image_url,
            content=content,
            court=court
        )

        category_ids = request.data.get("categories", [])
        post.categories.set(category_ids)

        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this post?
            self.check_object_permissions(request, post)

            serializer = SimplePostSerializer(post, data=request.data)
            if serializer.is_valid():
                # Update fields individually
                post.title = serializer.validated_data.get("title", post.title)
                post.image_url = serializer.validated_data.get("image_url", post.image_url)
                post.content = serializer.validated_data.get("content", post.content)

                # Handle court update separately
                court_id = serializer.validated_data.get("court", {}).get("id")
                if court_id is not None:
                    try:
                        post.court = Court.objects.get(pk=court_id)
                    except Court.DoesNotExist:
                        # Handle the case where the court does not exist
                        post.court = None

                post.save()

                category_ids = request.data.get("categories", [])
                post.categories.set(category_ids)

                updated_serializer = PostSerializer(post, context={"request": request})
                return Response(updated_serializer.data, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Court.DoesNotExist:
            # Handle the case where the specified court does not exist
            return Response({"detail": "The specified court does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(request, post)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
