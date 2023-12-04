from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from pickleapi.models import Post, PickleUser, Court
from django.contrib.auth.models import User
from .categories import CategorySerializer
from .users import PickleUserSerializer
from .categories import CategorySerializer


class SimplePostSerializer(serializers.ModelSerializer):
    # is_owner = serializers.SerializerMethodField()

    # def get_is_owner(self, obj):
    #     # Check if the authenticated user is the owner
    #     return self.context["request"].user == obj.pickle_user.user

    class Meta:
        model = Post
        fields = [
            "title",
            "image_url",
            "content",
            "categories",
            "court_id",
        ]


class PostSerializer(serializers.ModelSerializer):
    pickle_user = PickleUserSerializer(many=False)
    is_owner = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
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
            "court_id",
            "categories",
            "is_owner",
        ]


class PostViewSet(viewsets.ViewSet):
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
        # Get the data from the client's JSON payload
        pickle_user = PickleUser.objects.get(user=request.auth.user)
        title = request.data.get("title")
        publication_date = request.data.get("publication_date")
        image_url = request.data.get("image_url")
        content = request.data.get("content")
        court_id = request.data.get("court_id")

        court_instance, created = Court.objects.get_or_create(id=court_id)

        # Create a post database row first, so you have a
        # primary key to work with
        post = Post.objects.create(
            # maybe issues with pickle_user /  request.user
            pickle_user=pickle_user,
            title=title,
            publication_date=publication_date,
            image_url=image_url,
            content=content,
            court_id=court_instance
        )

        # Establish the many-to-many relationships
        category_ids = request.data.get("categories", [])
        post.categories.set(category_ids)

        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this post?
            self.check_object_permissions(request, post)

            serializer = SimplePostSerializer(data=request.data)
            if serializer.is_valid():
                # post.pickle_user = serializer.validated_data["pickle_user"]
                post.title = serializer.validated_data["title"]
                # post.publication_date = serializer.validated_data["publication_date"]
                post.image_url = serializer.validated_data["image_url"]
                post.content = serializer.validated_data["content"]
                post.court_id = serializer.validated_data["court_id"]
                post.save()

                category_ids = request.data.get("categories", [])
                post.categories.set(category_ids)

                serializer = PostSerializer(post, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(request, post)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
