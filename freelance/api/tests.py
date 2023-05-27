from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task, User, Customer, Tag, Bid, Executor


class TaskViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpasswordT123'
        )
        self.customer = Customer.objects.create(user=self.user)
        self.task1 = Task.objects.create(
            title='Task 1',
            description='Task 1 Description',
            customer=self.customer
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            description='Task 2 Description',
            customer=self.customer
        )
        self.tag = Tag.objects.bulk_create([Tag(name='Now'), Tag(name='Tomorrow')])

    def test_get_tasks(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        self.client.force_authenticate(user=self.user)
        tag_pks = [tag.pk for tag in self.tag]
        data = {
            'title': 'Task 3',
            'description': 'Task 3 Description',
            'tags': tag_pks
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(pk=response.data['id'])
        self.assertEqual(task.title, 'Task 3')
        self.assertEqual(task.description, 'Task 3 Description')
        self.assertEqual(task.customer, self.user.customer)
        self.assertEqual(task.tags.count(), 2)

    def test_update_task(self):
        self.client.force_authenticate(user=self.user)
        task = Task.objects.get(title='Task 1')
        tag_pks = [tag.pk for tag in self.tag]
        data = {
            'title': 'Task 1 Updated',
            'description': 'Task 1 Description Updated',
            'tags': tag_pks
        }
        response = self.client.patch(f'/api/tasks/{task.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Task 1 Updated')
        self.assertEqual(task.description, 'Task 1 Description Updated')
        self.assertEqual(task.tags.count(), 2)

    def test_delete_task(self):
        self.client.force_authenticate(user=self.user)
        task = Task.objects.get(title='Task 1')
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BidViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpasswordT123'
        )
        self.executor_user = User.objects.create_user(
            email='testexecutor@example.com',
            password='testpasswordT123'
        )
        self.customer = Customer.objects.create(user=self.user)
        self.executor = Executor.objects.create(user=self.executor_user)

        self.task = Task.objects.create(
            title='Task 1',
            description='Task 1 Description',
            customer=self.customer
        )

    def test_create_bid(self):
        self.client.force_authenticate(user=self.executor_user)

        data = {
            'task': self.task.id,
            'price': 100,
            'delivery_time': 6,
        }

        response = self.client.post(f'/api/tasks/{self.task.id}/bid/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bid.objects.count(), 1)

    def test_create_bid_with_zero_price(self):
        self.client.force_authenticate(user=self.executor_user)

        data = {
            'task': self.task.id,
            'price': 0,
            'delivery_time': 1,
        }

        response = self.client.post(f'/api/tasks/{self.task.id}/bid/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



