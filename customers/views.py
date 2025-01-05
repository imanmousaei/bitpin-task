from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Customer


class RegisterView(APIView):
    def post(self, request):
        body = request.POST
        phone_number = body.get('phone')
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        username = body.get('username')
        password = body.get('password')

        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, password=password)
        customer = Customer.objects.create(user=user, phone_number=phone_number)

        response = {
            'success': True,
        }
        return Response(response, status=status.HTTP_201_CREATED)
