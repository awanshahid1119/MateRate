from array import array
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from datetime import datetime
from .models import *
from .serializers import *
from .utils import *

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def take_notes(request):
    if request.method == 'GET':
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        # return JsonResponse({'notes': serializer.data}, safe=False)
        return Response(serializer.data)
    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            # note = serializer.save()
            # print(note)
            # get_feedback(note)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            request.session['note_data'] = serializer.validated_data
            return Response(serializer.data, status=status.HTTP_200_OK)
            # return JsonResponse({'note': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_note(request):
    note_data = request.session.get('note_data')
    if not note_data:
        return Response({'error': 'Note data not found.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = NoteSerializer(data=note_data)
    if serializer.is_valid():
        # note = serializer.save()
        note = serializer.save(user=request.user)
        print(note)
        del request.session['note_data']
        feedback = get_feedback(note.title, note.content)
        note.educator_feedback = feedback
        note.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PUT', 'DELETE'])  
@permission_classes([IsAuthenticated])  
def note_detail(request, id):
    try:
        note = Note.objects.get(pk=id, user=request.user)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        # return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method=='GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)
        # return JsonResponse({'note': serializer.data})
    elif request.method=='PUT':
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            temp = serializer.save()
            get_feedback(temp)
            temp.save()
            return Response(serializer.data)
            # return JsonResponse({'note': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        note.delete()
        return Response(status.HTTP_204_NO_CONTENT)
        # return JsonResponse({'error': 'No Content'}, status=204)