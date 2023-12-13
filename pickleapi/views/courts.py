from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from pickleapi.models import Court, PickleUser
from django.contrib.auth.models import User


class CourtSerializer(serializers.ModelSerializer):
    # is_owner = serializers.SerializerMethodField()

    # def get_is_owner(self, obj):
    #     # Check if the authenticated user is the owner
    #     return self.context["request"].user == obj.pickle_user.user

    class Meta:
        model = Court
        fields = [
            "id",
            "title",
            "court_image_url",
            "city",
            "state",
            "number_of_courts",
            "open_hours"
        ]



class CourtViewSet(viewsets.ViewSet):
    def list(self, request):
        courts = Court.objects.all()
        serializer = CourtSerializer(courts, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            court = Court.objects.get(pk=pk)
            serializer = CourtSerializer(court, context={"request": request})
            return Response(serializer.data)

        except Court.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        title = request.data.get("title")
        court_image_url = request.data.get("court_image_url")
        city = request.data.get("city")
        state = request.data.get("state")
        number_of_courts = request.data.get("number_of_courts")
        open_hours = request.data.get("open_hours")

        # Create a court database row first, so you have a
        # primary key to work with
        court = Court.objects.create(
            title=title,
            court_image_url=court_image_url,
            city=city,
            state=state,
            number_of_courts=number_of_courts,
            open_hours=open_hours
        )

        serializer = CourtSerializer(court, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            court = Court.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this court?
            self.check_object_permissions(request, court)

            serializer = CourtSerializer(data=request.data)
            if serializer.is_valid():
                # court.pickle_user = serializer.validated_data["pickle_user"]
                court.title = serializer.validated_data["title"]
                # court.publication_date = serializer.validated_data["publication_date"]
                court.court_image_url = serializer.validated_data["court_image_url"]
                court.city = serializer.validated_data["city"]
                court.state = serializer.validated_data["state"]
                court.number_of_courts = serializer.validated_data["number_of_courts"]
                court.open_hours = serializer._validated_data["open_hours"]
                court.save()

                serializer = CourtSerializer(court, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Court.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            court = Court.objects.get(pk=pk)
            self.check_object_permissions(request, court)
            court.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Court.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
