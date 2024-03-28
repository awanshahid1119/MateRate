from array import array
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics, permissions, exceptions, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from datetime import datetime
from .models import *
from .serializers import *
    

class AssignmentId(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    serializer_class = WorksheetSerializer
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Worksheet.objects.filter(id=self.kwargs['id'])

    def get(self, request, id):
        return self.retrieve(request, id)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
    
class Questions(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
    
class QuestionId(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if id:
            return self.retrieve(request, id)
        return JsonResponse({'error': 'Some Error'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        if id:
            return self.update(request, id)
        return JsonResponse({'error': 'Some Error'}, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, id):  ## DOUBT
    #     if id:
    #         return self.destroy(request, id)
    #     return Response("Option do not exist", status=status.HTTP_400_BAD_REQUEST)


def get_assignment_from_request(request):
    student = request.user.student

    # worksheets = student.worksheet_set.all().order_by('-id')
    worksheets = Worksheet.objects.filter(student=student)

    query_id = request.GET.get('id')

    serializer = WorksheetSerializer(data={'worksheet_id': query_id})
    serializer.is_valid(raise_exception=True)
    worksheet_id = serializer.validated_data['worksheet_id']

    worksheet = worksheets.filter(id=worksheet_id)[0]
    return worksheet


@api_view(['GET'])
@parser_classes([JSONParser])
@permission_classes([permissions.IsAuthenticated, ])
def assignment_intro(request):
    try:

        worksheet = get_assignment_from_request(request)

        worksheet_intro_details: array = worksheet.intro_details()

        RES = {
            **worksheet_intro_details
        }
        print(RES, "materate")
        return Response(RES, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(e, status=status.HTTP_403_FORBIDDEN)
    

