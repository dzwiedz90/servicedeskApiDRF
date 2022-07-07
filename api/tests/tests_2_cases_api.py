from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Case, User

HOST_URL = 'http://localhost:8000/'


class CaseApiTests(APITestCase):

    def setUp(self):
        self.user3 = User.objects.create(username='user1', password='password', email='user1@localhost.com',
                                         first_name='John', last_name='Doe', date_created=timezone.localtime(),
                                         is_active=True, is_admin=False, is_staff=False, is_superuser=False)
        self.admin3 = User.objects.create(username='admin1', password='password', email='admin1@localhost.com',
                                          first_name='John', last_name='Doe', date_created=timezone.localtime(),
                                          is_active=True, is_admin=True, is_staff=False, is_superuser=False)
        self.case1 = Case.objects.create(content='Szypko myszka sie pali', date_created=timezone.localtime(),
                                         severity=1, is_closed=False, user=self.user3, admin_assigned=None)
        self.case2 = Case.objects.create(content='Konkuter nie dziua', date_created=timezone.localtime(),
                                         severity=1, is_closed=False, user=self.user3, admin_assigned=self.admin3)

    def test_cases_get_all_cases(self):
        response = self.client.get(HOST_URL + 'cases/')
        cases = Case.objects.all()
        self.assertEqual(response.data[0]['content'], cases[0].content)
        self.assertEqual(response.data[1]['content'], cases[1].content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cases_create_case(self):
        request = self.client.post(HOST_URL + 'cases/',
                                   data={'content': 'Monitur nie swieci', 'severity': 1, 'user': 158}, format='json')
        response = self.client.get(HOST_URL + 'cases/')
        cases = Case.objects.all()
        self.assertEqual(response.data[len(response.data) - 1]['content'], cases[len(cases) - 1].content)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_cases_create_case_wrong_input_data(self):
        request = self.client.post(HOST_URL + 'cases/',
                                   data={'wrong_content': 'Monitur nie swieci', 'severity': 1, 'user': 158},
                                   format='json')
        case = Case.objects.last()
        self.assertNotEqual('Monitur nie swieci', case.content)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cases_create_case_no_input_data(self):
        request = self.client.post(HOST_URL + 'cases/')
        case = Case.objects.last()
        self.assertNotEqual(None, case.content)
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_cases(self):
        users = User.objects.all()
        request = self.client.get(HOST_URL + 'cases/user/170/')
        cases = Case.objects.all().filter(user=170)
        self.assertEqual(request.data[0]['id'], cases[0].id)
        self.assertEqual(request.data[1]['id'], cases[1].id)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_users_cases_wrong_id(self):
        users = User.objects.all()
        request = self.client.get(HOST_URL + 'cases/user/666/')
        cases = Case.objects.all().filter(user=666)
        self.assertEqual(len(cases), 0)
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_users_cases_no_id(self):
        pass

    def test_get_unassigned_cases(self):
        pass

    def test_get_archived_cases(self):
        pass

    def test_case_get_case(self):
        pass

    def test_case_get_case_wrong_id(self):
        pass

    def test_case_update_case(self):
        pass

    def test_case_update_case_wrong_id(self):
        pass

    def test_case_update_case_no_id(self):
        pass

    def test_case_delete_case(self):
        pass

    def test_case_delete_case_wrong_id(self):
        pass

    def test_case_delete_case_no_id(self):
        pass

    def test_case_delete_case_already_archived(self):
        pass

    def test_case_reopen_case(self):
        pass

    def test_case_reopen_case_wrong_id(self):
        pass

    def test_case_reopen_case_no_id(self):
        pass

    def test_case_reopen_case_not_archived(self):
        pass

    def test_assign_admin_to_case(self):
        pass

    def test_assign_admin_to_case_user_assigned_not_admin(self):
        pass

    def test_assign_admin_to_case_wrong_case_id(self):
        pass

    def test_assign_admin_to_case_no_case_id(self):
        pass

    def test_assign_admin_to_case_user_wrong_id(self):
        pass

    def test_assign_admin_to_case_user_no_id(self):
        pass

    def test_assign_admin_to_case_no_data_provided(self):
        pass
