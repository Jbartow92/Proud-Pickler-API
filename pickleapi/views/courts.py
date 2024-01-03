from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from pickleapi.models import Court
from django.contrib.auth.models import User


class CourtSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {
            "title": {"required": True},
            "court_image_url": {"required": True},
            "city": {"required": True},
            "state": {"required": True},
            "number_of_courts": {"required": True},
            "open_hours": {"required": True}
        }


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
        serializer = CourtSerializer(data=request.data)
        if serializer.is_valid():
            court = serializer.save()
            return Response(CourtSerializer(court, context={"request": request}).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            court = Court.objects.get(pk=pk)
            self.check_object_permissions(request, court)

            serializer = CourtSerializer(court, data=request.data)
            if serializer.is_valid():
                serializer.save()
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
