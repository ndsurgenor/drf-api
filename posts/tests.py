from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='admin', password='password123',
        )
    
    def test_can_list_posts(self):
        admin = User.objects.get(username='admin')
        Post.objects.create(owner=admin, title='post_title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(
            username='admin', password='password123',
        )
        response = self.client.post(
            '/posts/', {'title': 'post_title'},
        )
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post(
            '/posts/', {'title': 'post_title'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        user_a = User.objects.create_user(
            username='user_a', password='password123'
        )
        user_b = User.objects.create_user(
            username='user_b', password='password123'
        )
        Post.objects.create(
            owner=user_a, title='title a', content='content a'
        )
        Post.objects.create(
            owner=user_b, title='title b', content='content b'
        )
    
    def test_can_get_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'title a')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_get_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='user_a', password='password123')
        response = self.client.put('/posts/1/', {'title': 'title updated'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'title updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='user_a', password='password123')
        response = self.client.put('/posts/2/', {'title': 'title updated'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)