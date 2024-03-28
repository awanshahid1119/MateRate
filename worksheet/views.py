from array import array
from webbrowser import get
from xmlrpc.client import ResponseError
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics, permissions, exceptions, status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from student.models import *
from . import models
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
import json
from django.http import JsonResponse
from .utils import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_worksheet(request):
    if request.method == 'POST':
        name = request.data.get('name')
        description = request.data.get('description')
        classroom_ids = request.data.get('classroom', [])
        standard = request.data.get('standard')

        worksheet = Worksheet.objects.create(
            name=name,
            description=description,
            standard=standard,
            instructions=request.data.get('instructions'),
            isDraft=request.data.get('isDraft', False)
        )

        worksheet.classroom.add(*classroom_ids)

        return Response({'worksheet_id': worksheet.id, 'message': 'Worksheet created'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class WorksheetId(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
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
    
class QuestionView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
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
        return Response("some error", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        if id:
            return self.update(request, id)
        return Response("some error", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        if id:
            return self.destroy(request, id)
        return Response("Option do not exist", status=status.HTTP_400_BAD_REQUEST)
    
class SolutionView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
    
class SolutionId(RetrieveUpdateDestroyAPIView):
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()
    lookup_field = 'id'
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if id:
            return self.retrieve(request, id)
        return Response("Solution do not exist", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        if id:
            return self.update(request, id)
        return Response("Solution do not exist", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        if id:
            return self.destroy(request, id)
        return Response("Solution do not exist", status=status.HTTP_400_BAD_REQUEST)
    
def get_worksheet_from_request(request):
    student = request.user.student

    classroom = student.classroom

    worksheets = classroom.worksheet_set.all().order_by('-id')

    query_id = request.GET.get('id')

    serializer = WorksheetIdSerializer(data={'worksheet_id': query_id})
    serializer.is_valid(raise_exception=True)
    worksheet_id = serializer.validated_data['worksheet_id']

    assignment = worksheets.filter(id=worksheet_id)[0]
    return assignment

@api_view(['GET'])
@parser_classes([JSONParser])
@permission_classes([permissions.IsAuthenticated, ])
def worksheet_intro(request):
    try:

        worksheet = get_worksheet_from_request(request)

        worksheet_intro_details: array = worksheet.intro_details()

        RES = {
            **worksheet_intro_details
        }
        print(RES, "materate")
        return Response(RES, status=status.HTTP_200_OK)

    except Exception as e:
        print('1')
        print(e)
        return Response(e, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
@parser_classes([JSONParser])
@permission_classes([permissions.IsAuthenticated, ])
def worksheet_submit(request):

    try:
        received_json_data = json.loads(request.body.decode("utf-8"))

        student = request.user.student
        worksheet_id = request.data["id"]

        worksheet = Worksheet.objects.get(id=worksheet_id)

        responses = request.data["data"]["questions"]

        last_submission = student.student_submission.filter(
            worksheet=worksheet).first()

        if (last_submission is not None):
            last_submission.delete()

        submission = Submission.objects.create(
            student=student, assignment=worksheet)

        """last_response_model"""

        last_response_model = student.user_response.filter(
            worksheet_id=worksheet).last()

        """saving all the responses of student and increment number of attempts of assignment and leaderboard"""

        # if (last_response_model is not None):
        #     response_model = last_response_model
        #     response_model.total_attempts = last_response_model.total_attempts + 1

        # else:

        response_model = Response_model.objects.create(
            student_id=student, worksheet_id=worksheet)

        last_response_model = response_model if last_response_model == None else last_response_model

        response_model.time_stats = {}
        response_model.response_behaviour = {}
        response_model.responses.set([])
        for response in responses:

            question = worksheet.question_set.get(id=response['id'])

            response_time_stats = response_model.time_stats
            response_time_stats[response['id']] = response['time_taken']

            student_response_behaviour = response_model.response_behaviour

            student_response_behaviour[response['id']] = {}

            # student_response_behaviour[response['id']
            #                            ]['hintUsed'] = response['hintUsed']

            # student_response_behaviour[response['id']
            #                            ]['explanationUsed'] = response['explanationUsed']

            # option = question.option_set.get(id=response['selected_option'])
            # response_model.responses.add(option)

            solution = Solution.objects.get(question=question)
            feedback = get_feedback(question.question, solution.solution_steps, solution.final_answer)
            question.educator_feedback = feedback
            question.save()
            response_model.responses.add(solution)

            response_model.save()

        # """ delete progress id after saving all details in response"""

        # student_assignment_progress = async_models.Progress.objects.filter(
        #     student=student, assignment=assignment).first()

        # if (student_assignment_progress is not None):
        #     student_assignment_progress.delete()

        # """submission id of new submission"""

        RES = {
            'submission_id': submission.id
        }

        print(RES)

        submission.save()
        return Response(RES)

    except Exception as e:
        print(e)
        return Response(e, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@parser_classes([JSONParser])
@permission_classes([permissions.IsAuthenticated, ])
def display_graded_copy(request, worksheet_id):
    try:
        worksheet = Worksheet.objects.get(id=worksheet_id)
    except Worksheet.DoesNotExist:
        return Response({'error': 'Worksheet not found.'}, status=404)
    responses = Response_model.objects.filter(worksheet_id=worksheet)

    data = {
        'worksheet': {
            'name': worksheet.name,
            'description': worksheet.description,
        },
        'responses': []
    }

    for response in responses:
        response_data = {
            'id': response.id,
            'student_id': response.student_id,
            'solutions': []
        }

        for solution in response.responses.all():
            solution_data = {
                'question_name': solution.question.name,
                'final_answer': solution.final_answer,
                'feedback': solution.question.educator_feedback,
                'resources': solution.question.resources
            }
            response_data['solutions'].append(solution_data)

        data['responses'].append(response_data)

    return Response(data)

@api_view(['GET'])
@parser_classes([JSONParser])
@permission_classes([permissions.IsAuthenticated])
def display_original_copy(request, worksheet_id):
    try:
        worksheet = Worksheet.objects.get(id=worksheet_id)
    except Worksheet.DoesNotExist:
        return Response({'error': 'Worksheet not found.'}, status=404)

    questions = Question.objects.filter(worksheet=worksheet)

    data = {
        'worksheet': {
            'name': worksheet.name,
            'description': worksheet.description,
            # Add more fields as needed
        },
        'questions': []
    }

    for question in questions:
        question_data = {
            'id': question.id,
            'name': question.name,
            'q_no': question.q_no,
            'question': question.question,
            'student_answers': []
        }

        for response in Response_model.objects.filter(worksheet_id=Worksheet):
            student_answer = response.responses.filter(question=question).first()
            if student_answer:
                question_data['student_answers'].append({
                    'student_id': response.student_id,
                    'final_answer': student_answer.final_answer,
                })

        data['questions'].append(question_data)

    return Response(data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, ])
def get_all_worksheets(request):
    worksheets = Worksheet.objects.all()

    data = []
    for worksheet in worksheets:
        worksheet_data = worksheet.details()
        data.append(worksheet_data)

    return Response(data)