from rest_framework import serializers
from .models import *


class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['name', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )

        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
