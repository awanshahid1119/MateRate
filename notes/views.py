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

@api_view(['GET', 'POST'])
def take_notes(request):
    
    if request.method == 'GET':
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return JsonResponse({'notes': serializer.data}, safe=False)
    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse({'note': serializer.data})

@api_view(['GET', 'PUT', 'DELETE'])    
def note_detail(request, id):

    try:
        note = Note.objects.get(pk=id, user=request.user)
    except Note.DoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'error': 'Not found'}, status=404)
    
    if request.method=='GET':
        serializer = NoteSerializer(note)
        # return Response(serializer.data)
        return JsonResponse({'note': serializer.data})
    elif request.method=='PUT':
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return JsonResponse({'note': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        note.delete()
        # return Response(status.HTTP_204_NO_CONTENT)
        return JsonResponse({'error': 'No Content'}, status=204)