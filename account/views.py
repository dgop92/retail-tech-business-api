from account.custom_auth import BearerTokenAuthentication
from account.custom_filters import MyUsersFilter
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from account.custom_permissions import IsSuperUser

from .models import MyUser, Profile
from .serializers import ProfileSerializer, RegisterSerializer, UserSerializer

ACCOUNT_AUTH_CLASSES = (BearerTokenAuthentication, )

class UserList(generics.ListAPIView):

    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    name = "user-list"

    search_fields = (
        '$username',
        '$email',
        '^first_name',
        '^last_name',
        '^profile__tice',
        '^profile__cellphone',
    )
    filter_class = MyUsersFilter
    ordering_fields = (
        'profile__date_of_birth',
        'profile__age',
        'username'
    )

    authentication_classes = ACCOUNT_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUser)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    name = "register-view"

    authentication_classes = ACCOUNT_AUTH_CLASSES
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.pop("password_confirmation")
            serializer.save()
            return Response(
                serializer.validated_data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    name = "profile-view"

    authentication_classes = ACCOUNT_AUTH_CLASSES
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ApiRoot(generics.GenericAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "user-list": reverse(UserList.name, request=request),
                "profile-detail": reverse(
                    ProfileDetailView.name, 
                    request=request
                ),
                "register": reverse(RegisterView.name, request=request),
            }
        )
