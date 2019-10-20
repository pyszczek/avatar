from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers


class AvatarActivationView(APIView):
    def get(self, request, user_uuid):
        raise Http404()

    def post(self, request, user_uuid):
        serializer = serializers.AvatarActivationSerializer(data=request.data, user_uuid=user_uuid)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        jwt = serializer.save()
        resp_data = {
            'jwt': jwt,
        }

        return Response(data=resp_data, status=status.HTTP_200_OK)
