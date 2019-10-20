import logging

from rest_framework import serializers
from rest_framework.fields import empty

from . import models, auth_jwt

logger = logging.getLogger(__name__)


class AvatarActivationSerializer(serializers.Serializer):
    otp = serializers.CharField()

    def __init__(self, instance=None, data=empty, user_uuid=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user_uuid = user_uuid

    def validate(self, attrs):
        attrs = super().validate(attrs)
        otp = attrs['otp']

        try:
            user = models.User.objects.get_by_uuid(user_uuid=self.user_uuid, otp=otp, is_active=False)
        except models.User.DoesNotExist:
            raise serializers.ValidationError({'uuid': ['Invalid value.']})

        attrs['user'] = user

        return attrs

    def update(self, instance, validated_data):
        return self.create(validated_data)

    def create(self, validated_data):
        user: models.User = validated_data['user']
        user.activate()

        jwt = auth_jwt.generate_jwt(
            sub=auth_jwt.SUB_AVATAR_ACTIVATEION,
            name=user.uuid,
            roles=[models.UserGroup.USER.value],
            secret_key=user.secret_key
        )

        return jwt
