from rest_framework import serializers
from .models import Task, Tag, Bid


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    tag_names = serializers.SerializerMethodField()

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
        executor = self.context['user'].executor
        task_id = self.context.get('task_id')
        bid = Bid.objects.create(user=user, task_id=task_id, executor=executor, **validated_data)
        return bid

# TODO написать сериаолизатор с методом get( получение списка всех заявок)
