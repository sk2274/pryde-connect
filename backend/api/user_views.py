from rest_framework import generics, status
from .serializers import UserSerializer, LoggedInUserSerializer, UserShortSerializer
from .models import Project, PUser, ResearchInterestUser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import CanEditDeleteUser
from rest_framework.parsers import MultiPartParser, FormParser
import os


class UserList(generics.ListAPIView):
    serializer_class = UserShortSerializer
    queryset = PUser.objects.filter(is_staff=False)


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = PUser.objects.filter(is_staff=False)


class LoggedInUserView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = PUser.objects.get(pk=request.user.pk)
        serializer = LoggedInUserSerializer(user, context={ 'request': request })
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UploadOrChangeProfilePicture(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [CanEditDeleteUser & IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            user = PUser.objects.get(pk=request.user.pk)
            self.check_object_permissions(request, user)

            if user.profile_picture:
                os.remove(user.profile_picture.path)
                user.profile_picture = request.data['file']
                # user.full_clean()
                user.save()
                return Response(data=UserShortSerializer(user).data, status=status.HTTP_201_CREATED)

            else:
                user.profile_picture = request.data['file']
                # user.profile_picture.validate()
                user.save()
                return Response(data=UserShortSerializer(user).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong while uploading your profile picture.'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [CanEditDeleteUser & IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        try:
            user = PUser.objects.get(pk=request.user.pk)
            self.check_object_permissions(request, user)

            user.locatedAtCornell = request.data['locatedAtCornell']
            user.locatedAtCCE = request.data['locatedAtCCE']
            user.role = request.data['role']
            user.displayRole = request.data['displayRole']
            user.affiliation = request.data['affiliation']
            user.location = request.data['location']
            user.email = request.data['email']
            user.phone = request.data['phone']
            user.website = request.data['website']
            user.researchDescription = request.data['researchDescription']
            user.roles = request.data['roles']
            user.ageRanges = request.data['ageRanges']
            user.deliveryModes = request.data['deliveryModes']
            user.researchNeeds = request.data['researchNeeds']
            user.evaluationNeeds = request.data['evaluationNeeds']

            user.save()

            ResearchInterestUser.objects.filter(user=user.pk).delete()
            for new_interest in request.data['researchInterests']:
                ResearchInterestUser.objects.create(user=user, researchInterest=new_interest)

            return Response(data=UserShortSerializer(user).data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong while updating your profile.'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [CanEditDeleteUser & IsAuthenticated, ]
    queryset = PUser.objects.filter(is_staff=False)
