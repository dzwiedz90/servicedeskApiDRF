from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User

HOST_URL = 'http://localhost:8000/'


class UsersApiTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='password', email='user1@localhost.com',
                                         first_name='John', last_name='Doe', date_created=timezone.localtime(),
                                         is_active=True, is_admin=False, is_staff=False, is_superuser=False)
        self.user2 = User.objects.create(username='user2', password='password', email='user2@localhost.com',
                                         first_name='John', last_name='Doe', date_created=timezone.localtime(),
                                         is_active=False, is_admin=False, is_staff=False, is_superuser=False)
        self.admin1 = User.objects.create(username='admin1', password='password', email='admin1@localhost.com',
                                          first_name='John', last_name='Doe', date_created=timezone.localtime(),
                                          is_active=True, is_admin=True, is_staff=False, is_superuser=False)
        self.admin2 = User.objects.create(username='admin2', password='password', email='admin2@localhost.com',
                                          first_name='John', last_name='Doe', date_created=timezone.localtime(),
                                          is_active=False, is_admin=True, is_staff=False, is_superuser=False)

    def test_users_get_all_users(self):
        response = self.client.get(HOST_URL + 'users/')
        users = User.objects.all().filter(is_active=True)
        self.assertEqual(response.data[0]['username'], users[0].username)
        self.assertEqual(response.data[1]['username'], users[1].username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_create_user(self):
        request = self.client.post(HOST_URL + 'users/', data={'username': 'new_user', 'password': 'new_password',
                                                              'email': 'new_user@localhost.com', 'first_name': 'Johnny',
                                                              'last_name': 'Doeowsky', 'is_admin': 'False'},
                                   format='json')
        response = self.client.get(HOST_URL + 'users/')
        users = User.objects.all().filter(is_active=True)
        self.assertEqual(response.data[len(response.data) - 1]['username'], users[len(users) - 1].username)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_users_create_user_wrong_input_data(self):
        request = self.client.post(HOST_URL + 'users/', data={'wrong_username': 'new_user', 'password': 'new_password',
                                                              'email': 'new_user@localhost.com', 'first_name': 'Johnny',
                                                              'last_name': 'Doeowsky', 'is_admin': 'False'},
                                   format='json')
        response = self.client.get(HOST_URL + 'users/')
        users = User.objects.all().filter(is_active=True)
        self.assertNotEqual(response.data[len(response.data) - 1]['username'], 'new_user')
        self.assertNotEqual(users[len(users) - 1].username, 'new_user')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_create_user_no_data(self):
        request = self.client.post(HOST_URL + 'users/', data={}, format='json')
        response = self.client.get(HOST_URL + 'users/')
        users = User.objects.all().filter(is_active=True)
        self.assertNotEqual(response.data[len(response.data) - 1]['username'], '')
        self.assertNotEqual(users[len(users) - 1].username, '')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_only_users(self):
        request = self.client.get(HOST_URL + 'users/users/')
        users = User.objects.all().filter(is_admin=False)
        self.assertEqual(request.data[0]['username'], users[0].username)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_only_admins(self):
        request = self.client.get(HOST_URL + 'users/admins/')
        users = User.objects.all().filter(is_admin=True)
        self.assertEqual(request.data[0]['username'], users[0].username)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_archived_users_all(self):
        request = self.client.get(HOST_URL + 'users/archived/all/', format='json')
        users = User.objects.all().filter(is_active=False)
        self.assertEqual(request.data[0]['username'], users[0].username)
        self.assertEqual(request.data[1]['username'], users[1].username)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_archived_users_users(self):
        request = self.client.get(HOST_URL + 'users/archived/users/', format='json')
        users = User.objects.all().filter(is_active=False, is_admin=False)
        self.assertEqual(request.data[0]['username'], users[0].username)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_archived_users_admins(self):
        request = self.client.get(HOST_URL + 'users/archived/admins/', format='json')
        users = User.objects.all().filter(is_active=False, is_admin=True)
        self.assertEqual(request.data[0]['username'], users[0].username)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_archived_users_no_type_provided(self):
        request = self.client.get(HOST_URL + 'users/archived/', format='json')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_archived_users_wrong_type_provided(self):
        request = self.client.get(HOST_URL + 'users/archived/wrong_type/', format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(request.data['message'], 'Wrong type data specified')

    def test_get_archived_users_empty_type_provided(self):
        request = self.client.get(HOST_URL + 'users/archived/ /', format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(request.data['message'], 'Wrong type data specified')

    def test_get_user(self):
        request = self.client.get(HOST_URL + 'users/61/', format='json')
        user = User.objects.get(id=61)
        self.assertEqual(request.data['username'], user.username)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_user_user_not_matching_id(self):
        request = self.client.get(HOST_URL + 'users/420/', format='json')
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=420)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_no_id(self):
        request = self.client.get(HOST_URL + 'users/ /', format='json')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        request = self.client.put(HOST_URL + 'users/85/',
                                  data={'email': 'new_email@localhost.com', 'first_name': 'New_name',
                                        'last_name': 'New_surname', 'is_admin': 'False', 'is_staff': 'False',
                                        'is_superuser': 'False'})
        user = User.objects.get(id=85)
        self.assertEqual(user.email, 'new_email@localhost.com')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_update_user_wrong_input_data(self):
        request = self.client.put(HOST_URL + 'users/97/', data={'email': 'new_email@localhost.com'})
        user = User.objects.get(id=97)
        self.assertNotEqual(user.email, 'new_email@localhost.com')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_no_input_data(self):
        request = self.client.put(HOST_URL + 'users/89/')
        user = User.objects.get(id=89)
        self.assertNotEqual(user.email, 'new_email@localhost.com')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_user_not_matching_id(self):
        request = self.client.put(HOST_URL + 'users/420/',
                                  data={'email': 'new_email@localhost.com', 'first_name': 'New_name',
                                        'last_name': 'New_surname', 'is_admin': 'False', 'is_staff': 'False',
                                        'is_superuser': 'False'})
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(id=420)
            self.assertNotEqual(user.email, 'new_email@localhost.com')
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        request = self.client.delete(HOST_URL + 'users/17/')
        user = User.objects.get(id=17)
        self.assertEqual(user.is_active, False)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_user_user_already_deleted(self):
        user = User.objects.get(id=22)
        self.assertEqual(user.is_active, False)
        request = self.client.delete(HOST_URL + 'users/22/')
        user = User.objects.get(id=22)
        self.assertEqual(user.is_active, False)
        self.assertEqual(request.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_delete_user_user_not_matching_id(self):
        request = self.client.delete(HOST_URL + 'users/420/')
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(id=420)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_restore_deleted_user(self):
        request = self.client.patch(HOST_URL + 'users/74/')
        user = User.objects.get(id=74)
        self.assertEqual(user.is_active, True)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_restore_deleted_user_user_not_deleted(self):
        user = User.objects.get(id=77)
        self.assertEqual(user.is_active, True)
        request = self.client.patch(HOST_URL + 'users/77/')
        user = User.objects.get(id=77)
        self.assertEqual(user.is_active, True)
        self.assertEqual(request.status_code, status.HTTP_304_NOT_MODIFIED)

    def test_restore_deleted_user_user_not_matching_id(self):
        request = self.client.patch(HOST_URL + 'users/420/')
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(id=420)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_password(self):
        request = self.client.put(HOST_URL + 'users/password/reset/1/', data={'password': 'new_password'})
        user = User.objects.get(id=1)
        self.assertEqual(user.password, 'new_password')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_change_password_user_not_matching_id(self):
        request = self.client.put(HOST_URL + 'users/password/reset/420/', data={'password': 'new_password'})
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(id=420)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_password_misspelled_parameter(self):
        request = self.client.put(HOST_URL + 'users/password/reset/9/', data={'password_wrong': 'new_password'})
        user = User.objects.get(id=9)
        self.assertNotEqual(user.password, 'new_password')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_missing_parameter(self):
        request = self.client.put(HOST_URL + 'users/password/reset/5/')
        user = User.objects.get(id=5)
        self.assertNotEqual(user.password, 'new_password')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
