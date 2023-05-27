from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from api.models import Task, Tag, Bid, User, Category, Profile


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    tag_names = serializers.SerializerMethodField()
    category = CategorySerializer()

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def create(self, validated_data):
        customer = self.context['request'].user.customer
        tags = validated_data.pop('tags')
        task = Task.objects.create(customer=customer, **validated_data)
        task.tags.set(tags)
        return task

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'customer', 'category', 'tags', 'tag_names']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'customer': {'read_only': True},
        }


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'task', 'executor', 'price', 'delivery_time']
        extra_kwargs = {
            'executor': {'read_only': True},
        }

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError('Это поле не может быть равно нулю')
        else:
            return price

    def create(self, validated_data):
        user = self.context.get('user')
        try:
            executor = self.context['user'].executor
        except AttributeError:
            raise AuthenticationFailed('Необходимо авторизоваться')
        task_id = self.context.get('task_id')
        bid = Bid.objects.create(user=user, task_id=task_id, executor=executor, **validated_data)
        return bid


# TODO написать сериаолизатор с методом get( получение списка всех заявок)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ProfileGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'user', 'location', 'birth_date']
        extra_kwargs = {
            'user': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'location': {'read_only': True},
            'birth_date': {'read_only': True}
        }


# todo использовать для смены всего кроме почты
class ProfilePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'user', 'location', 'birth_date']
        extra_kwargs = {
            'user': {'read_only': True}
        }

        @staticmethod
        def update(instance, validated_data):
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.location = validated_data.get('location', instance.location)
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.save()
            return instance


# todo использовать при РЕГИСТРАЦИИ
class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['user']
        try:
            profile = Profile.objects.create(user=user, **validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Профиль с такой почтой уже существует")
        return profile
