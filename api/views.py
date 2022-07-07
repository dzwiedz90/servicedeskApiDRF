from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User, Case, CaseUpdate
from .serializers.user_serializers import GetUsersSerializer, CreateUserSerializer, UpdateUserSerializer
from .serializers.case_serializers import GetCasesSerializer, CreateCaseSerializer, UpdateCaseSerializer
from .serializers.case_update_serializers import GetCaseUpdatesSerializer, CreateCaseUpdateSerializer


# USERS API

@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all().filter(is_active=True)
        serializer = GetUsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        request_data = request.data
        request_data['date_created'] = timezone.localtime()
        request_data['is_active'] = True
        request_data['is_staff'] = False
        request_data['is_superuser'] = False
        serializer = CreateUserSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Can\'t create user, wrong data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_only_users(request):
    users = User.objects.all().filter(is_admin=False, is_active=True)
    serializer = GetUsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_only_admins(request):
    users = User.objects.all().filter(is_admin=True, is_active=True)
    serializer = GetUsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_archived_users(request, type):
    """Takes in argument request.data['type'] to specify type of returned data:
        all, users, admins
    """
    try:
        if type == 'all':
            users = User.objects.all().filter(is_active=False)
        elif type == 'admins':
            users = User.objects.all().filter(is_admin=True, is_active=False)
        elif type == 'users':
            users = User.objects.all().filter(is_admin=False, is_active=False)
        serializer = GetUsersSerializer(users, many=True)
        return Response(serializer.data)
    except KeyError:
        return Response({'message': 'Type not specified'}, status=status.HTTP_400_BAD_REQUEST)
    except UnboundLocalError:
        return Response({'message': 'Wrong type data specified'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def user(request, id):
    try:
        user = User.objects.get(id=id)
        if request.method == 'GET':
            serializer = GetUsersSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UpdateUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.update(user, serializer.validated_data)
                return Response({'message': 'User updated'}, status=status.HTTP_200_OK)
            return Response({'message': 'Cant modify user, wrong data'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if user.is_active == True:
                user.is_active = False
                user.save()
                return Response({'message': 'User archived'})
            return Response({'message': 'User is already archived'}, status=status.HTTP_304_NOT_MODIFIED)
        elif request.method == 'PATCH':
            if user.is_active == False:
                user.is_active = True
                user.save()
                return Response({'message': 'User restored'}, status=status.HTTP_200_OK)
            return Response({'message': 'User was not archived'}, status=status.HTTP_304_NOT_MODIFIED)
    except User.DoesNotExist:
        return Response({'message': 'User with provided id does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def change_password(request, id):
    try:
        user = User.objects.get(id=id)
        user.password = request.data['password']
        user.save()
        return Response({'message': 'Password reset'})
    except User.DoesNotExist:
        return Response({'message': 'User with provided id does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except MultiValueDictKeyError:
        return Response({'message': 'Password not specified'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'message': 'Password not specified'}, status=status.HTTP_400_BAD_REQUEST)


# CASES API

@api_view(['GET', 'POST'])
def cases(request):
    if request.method == 'GET':
        cases = Case.objects.all().filter(is_closed=False)
        serializer = GetCasesSerializer(cases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        request_data = request.data
        request_data['date_created'] = timezone.localtime()
        request_data['is_closed'] = False
        request_data['admin_assigned'] = None
        serializer = CreateCaseSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Case created'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Can\'t create case, wrong data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_cases(request, id):
    cases = Case.objects.all().filter(user=id)
    if cases:
        serializer = GetCasesSerializer(cases, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'No cases found for give id'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_unassigned_cases(request):
    unassigned_cases = Case.objects.all().filter(admin_assigned=None)
    serializer = GetCasesSerializer(unassigned_cases, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_archived_cases(request):
    archived_cases = Case.objects.all().filter(is_closed=True)
    serializer = GetCasesSerializer(archived_cases, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def case(request, id):
    try:
        case = Case.objects.get(id=id)
        if request.method == 'GET':
            serializer = GetCasesSerializer(case)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UpdateCaseSerializer(case, data=request.data)
            if serializer.is_valid():
                serializer.update(case, serializer.validated_data)
                return Response({'message': 'Case updated'}, status=status.HTTP_200_OK)
            return Response({'message': 'Cant modify case, wrong data'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if not case.is_closed:
                case.is_closed = True
                case.save()
                return Response({'message': 'Case archived'})
            return Response({'message': 'Case is already archived'}, status=status.HTTP_304_NOT_MODIFIED)
        elif request.method == 'PATCH':
            if case.is_closed:
                case.is_closed = False
                case.save()
                return Response({'message': 'Case reopened'})
            return Response({'message': 'Case is not archived'}, status=status.HTTP_304_NOT_MODIFIED)
    except Case.DoesNotExist:
        return Response({'message': 'Case with matching id not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def assign_admin_to_case(request):
    try:
        case = Case.objects.get(id=request.data['case_id'])
        admin = User.objects.get(id=request.data['admin_id'])
        if admin.is_admin:
            case.admin_assigned = admin
            case.save()
            return Response({'message': 'Admin assigned'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'User assigned is not an admin'}, status=status.HTTP_400_BAD_REQUEST)
    except Case.DoesNotExist:
        return Response({'message': 'Case with matching id not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'message': 'User with matching id not found'}, status=status.HTTP_404_NOT_FOUND)


# CASE UPDATES API

@api_view(['GET', 'POST'])
def updates(request):
    if request.method == 'GET':
        case_update = CaseUpdate.objects.all()
        serializer = GetCaseUpdatesSerializer(case_update, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        request_data = request.data
        request_data['date_created'] = timezone.localtime()
        serializer = CreateCaseUpdateSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Case update created'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Can\'t create case update, wrong data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def update(request, id):
    try:
        case_update = CaseUpdate.objects.get(id=id)
        if request.method == 'GET':
            serializer = GetCaseUpdatesSerializer(case_update)
            return Response(serializer.data)
    except CaseUpdate.DoesNotExist:
        return Response({'message': 'Case update with matching id not found'}, status=status.HTTP_404_NOT_FOUND)
