from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from .forms import SignUpForm
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import random
from django.core.mail import EmailMessage

@api_view(['GET'])
def welcome_page(request):
    return Response({"msg": "Welcome to get an amazing experience"}, status=200)

@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def UserStudentRegistration(request):

    try:
        # print("materate", request.data)
        fire = request.data

        classes = {
            "1": "Class 1",
            "2": "Class 2",
            "3": "Class 3",
            "4": "Class 4",
            "5": "Class 5",
            "6": "Class 6",
            "7": "Class 7",
            "8": "Class 8",
            "9": "Class 9",
            "10": "Class 10",
        }

        classroom1 = Classroom.objects.get(name=classes[fire["standard"]])

        if User.objects.filter(username=fire['email']):

            f = User.objects.get(username=fire['email'])

            if Student.objects.filter(user=f):
                student1 = Student.objects.get(user=f)
                student1.classroom = classroom1
                student1.name = fire['name']
                student1.contact_no = fire['guardian_contact']
                student1.standard = fire['standard']
                student1.save()
                RES = "User and student are already added"

            else:

                Student.objects.create(user=f, classroom=classroom1, premium_user="0",
                                       name=fire['name'], email=fire['email'], contact_no=fire['guardian_contact'], standard=fire["standard"])

                RES = "Added student successfully"

        else:
            s = User.objects.create_user(
                username=fire['email'],
            )
            pass1 = "materate@123"
            s.set_password(pass1)
            s.save()

            user = User.objects.get(username=fire['email'])

            Student.objects.create(user=user, classroom=classroom1, premium_user="0",
                                   name=fire['name'], email=fire['email'], contact_no=fire['guardian_contact'], standard=fire["standard"])

            # messenger = WhatsApp(token=API_TOKEN, phone_number_id=SENDER_ID)
            # messenger.send_message(
            #     f"Your username , password is {fire['email']} and {pass1}", f"91{fire['guardian_contact']}")
            # messenger.send_message(
            #     "Disclaimer: This is the dummy password to login to your account first time. Please reset this password to protect your account", f"91{fire['guardian_contact']}")

            RES = "Added User and student successfully"

        return Response(RES)
    except Exception as e:
        print(e)
        return Response(e)
    
def user_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@api_view(['GET'])
@permission_classes([permissions.AllowAny, ])
def isValid_User(request):
    try:
        student_username = request.data['email']
        user = User.objects.filter(username=student_username).first()

        if (user is None):
            return Response("Username is not found", status=status.HTTP_404_NOT_FOUND)

        return Response("Username is validated , now you ready to go!", status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(e)
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        """Blacklist the refresh token: extract token from the header
      during logout request user and refresh token is provided"""
        try:
            serializer = LogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            refresh_token = validated_data["refresh_token"]
            token = RefreshToken(refresh_token)
            # token = RefreshToken(base64_encoded_token_string)
            token.blacklist()
            logout(request)
            # logout(request, token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(generics.GenericAPIView):
    """
    To Authenticate a user and return necessary details.
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(request, username=username, password=password)
        if Student.objects.filter(user=user):
            login(request, user)

            tokens = get_tokens_for_user(user)
            return Response({
                'detail': 'ok',
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'user_type': 'student'
            })
        else:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

class ChangeUsernameView(generics.GenericAPIView):
    """
    To Change username of an Authenticated User depending on
    has_changed_username property of the user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ChangeUsernameSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'detail': 'ok'}
        return Response(data=data)
    
class ChangePasswordView(generics.GenericAPIView):
    """
    To Change password of an Authenticated User.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'detail': 'ok'}
        return Response(data=data)
    
class StudentView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = StudentSerializer
    lookup_field = 'user'

    def get_object(self):
        return get_object_or_404(Student, user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = get_object_or_404(Student, user=self.request.user)
        for key in request.data:
            setattr(student, key, request.data[key])
        student.save()
        data = {'detail': 'ok'}
        return Response(data=data)
    
@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def CheckOTP(request):

    try:

        otp = request.data['otp']
        email = request.data['username']
        if Student.objects.filter(email=email).exists():
            student = Student.objects.get(email=email)
            forget_password_token = student.forget_password_token
            if forget_password_token != otp:
                return Response('Invalid otp')
            else:
                token = ''
                for i in range(0, 4):
                    n = random.randint(0, 9)
                    token = token + str(n)

                student.forget_password_token = token
                student.save()
                return Response('Valid otp')

    except Exception as e:
        print(e)
        return Response(e)


# password reset
class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request, *args, **kwargs):
        data = {'request': request, 'data': request.data}
        serializer = self.get_serializer(data=data)

        email = request.data['email']
        if Student.objects.filter(email=email):

            user = Student.objects.get(email=email)

            token = ''
            for i in range(0, 4):
                n = random.randint(0, 9)
                token = token + str(n)

            email_body = 'Hello,\n Use this otp to reset your password ' + token
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your password'
            }

            Util.send_email(data)

            user.forget_password_token = token

            user.save()

            return Response({'succes': 'We have sent you an otp to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response("User with this email id doesn't exist")


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[
                data['to_email']]
        )
        email.send()


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def SetNewPasswordAPIView(request):
    # serializer_class = SetNewPasswordSerializer
    # def patch(self,request):
    # data = {'request': request , 'data' : request.data}
    # serializer = self.get_serializer(data=data)

    email = request.data['email']
    new_password = request.data['new_password']

    if Student.objects.filter(email=email).exists():
        user = Student.objects.get(email=email)

        user.user.set_password(new_password)
        user.save()
        return Response({'Password Reset Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response('failed')


# change password


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, ])
def changeProfilePassword(request):
    """
    Input - old password and new password
    Output - profile password of user set to new password
    """
    try:
        old_password = request.data['old_password']

        new_password = request.data['new_password']

        user = request.user

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response("Password changed successfully", status=status.HTTP_200_OK)
        else:
            return Response("Incorrect Password")

    except Exception as e:
        print(e)
        return Response(e)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, ])
def savestudentprofile(request):

    try:
        profile = request.data
        user1 = request.user

        student_data = Student.objects.get(user=user1)
        if (profile["name"]):
            student_data.name = profile["name"]
        if (profile["standard"]):
            student_data.standard = profile["standard"]
        if (profile["email"]):
            student_data.email = profile["email"]
        if (profile["contact_no"]):
            student_data.contact_no = profile["contact_no"]
        student_data.guardian_name = profile["guardian_name"]
        student_data.guardian_address = profile["guardian_address"]
        if (profile["school"]):
            student_data.school_name = profile["school"]

        student_data.save()

        RES = "Saved successfully"
        print(RES)
        return Response(RES)
    except Exception as e:
        print(e)
        return Response(e)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, ])
def studentprofile(request):
    """
    Input:
    Output: name, standard, email, contact_no, guardian_name, guardian_address, school
    """

    try:

        student = request.user.student

        RES = {
            'name': student.name,
            'standard': student.standard,
            'school': student.school_name,
            'guardian_address': student.guardian_address,
            'guardian_name': student.guardian_name,
            'email': student.email,
            'contact_no': student.contact_no,
        }

        return Response(RES)

    except ObjectDoesNotExist:
        raise exceptions.NotFound("No entry found")

