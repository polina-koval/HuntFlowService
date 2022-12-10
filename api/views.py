from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from api.serializers import UserSerializer
import requests


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        res = requests.get(
            "https://dev-100-api.huntflow.dev/v2/me",
            headers={
                "Authorization": f"Bearer {settings.API_KEY_HF}",
            },
        )
        print(res.content)
        return Response(serializer.data)


class VacancyWebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        body = request.data
        print(body)
        return Response({}, status=status.HTTP_200_OK)
