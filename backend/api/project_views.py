from rest_framework import generics, status
from .serializers import ProjectSerializer, ProjectShortSerializer, ProjectUpdateSerializer
from .models import Project, PUser, TopicsProject, DeliveryModeProject
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

# custom permissions
from .permissions import CanDeleteProject, CanEditProject


class ProjectList(generics.ListAPIView):
    serializer_class = ProjectShortSerializer
    queryset = Project.objects.filter(isApproved=True)


class ProjectView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.filter(isApproved=True)


class CreateProject(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Project.objects.filter(isApproved=True)

    #TODO: THE PLACEMENT OF THE TRY BLOCKS MIGHT BE MESSED UP

    def post(self, request, *args, **kwargs):
        user = PUser.objects.get(pk=request.user.pk)
        try:
            new_project = Project.objects.create(
                name=request.data['name'],
                owner=user,
                status=request.data['status'],
                summary=request.data['summary'],
                # researchTopics=request.data['researchTopics'],
                ageRanges=request.data['ageRanges'],
                # deliveryModes=request.data['deliveryModes'],
                timeline=request.data['timeline'],
                commitmentLength=request.data['timeline'],
                incentives=request.data['incentives'],
                additionalInformation=request.data['additionalInformation'],
                # additionalFiles = request.data['additionalFiles'], # TODO: this probably needs changing
                alternateContact=request.data['alternateContact'],
                alternateLocation=request.data['alternateLocation']
            )

            for mode in request.data['deliveryModes']:
                try:
                    DeliveryModeProject.objects.create(project=new_project, deliveryMode=mode)
                except Exception as e:
                    print(e)

            for topic in request.data['researchTopics']:
                try:
                    TopicsProject.objects.create(project=new_project, researchTopic=topic)
                except Exception as e:
                    print(e)

            return Response({'data': ProjectSerializer(new_project).data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'status': 'Something went wrong while creating the project.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateProject(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [CanEditProject & IsAuthenticated, ]
    # serializer_class = ProjectUpdateSerializer
    # queryset = Project.objects.filter(isApproved=True)

    def put(self, request, *args, **kwargs):
        print("updating object")

        try:

            project = Project.objects.get(pk=kwargs['pk'])

            if 'name' in request.data:
                project.name = request.data['name']
            if 'status' in request.data:
                project.status = request.data['status']
            if 'summary' in request.data:
                project.summary = request.data['summary']
            if 'ageRanges' in request.data:
                project.ageRanges = request.data['ageRanges']
            if 'timeline' in request.data:
                project.timeline = request.data['timeline']
            if 'commitmentLength' in request.data:
                project.commitmentLength = request.data['commitmentLength']
            if 'incentives' in request.data:
                project.incentives = request.data['incentives']
            if 'additionalInformation' in request.data:
                project.additionalInformation = request.data['additionalInformation']
            if 'type' in request.data:
                project.type = request.data['type']
            if 'alternateContact' in request.data:
                project.alternateContact = request.data['alternateContact']
            if 'alternateLocation' in request.data:
                project.alternateLocation = request.data['alternateLocation']

            project.save()

            if 'researchTopics' in request.data:
                current_topics = TopicsProject.objects.filter(project=project.pk)
                for topic in current_topics:
                    topic.delete()
                for new_topic in request.data['researchTopic']:
                    TopicsProject.objects.create(project=project.pk, researchTopic=new_topic)
            if 'deliveryMode' in request.data:
                current_deliveryModes = DeliveryModeProject.objects.filter(project=project.pk)
                for mode in current_deliveryModes:
                    mode.delete()
                for new_mode in request.data['deliveryMode']:
                    DeliveryModeProject.objects.create(project=project.pk, deliveryMode=new_mode)

            return Response(data=ProjectShortSerializer(project).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)



class DeleteProject(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [CanDeleteProject & IsAuthenticated, ]
    queryset = Project.objects.filter(isApproved=True)