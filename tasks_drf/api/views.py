
from .custom.api_response import ApiResponse
from .serializers import TaskSerializer
from .models import Task
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

class TaskViewSet(viewsets.ViewSet):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user   
        search = request.GET['search']        
        if not search:
            queryset = Task.objects.filter(user_id=user.id).order_by('-created_at')            
        else:
            queryset = Task.objects.filter(user_id=user.id, description__icontains=search).order_by('-created_at')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = TaskSerializer(page, many=True)        
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = TaskSerializer(queryset, many=True)
            return ApiResponse.Success(serializer.dat)         
    
    def retrieve(self, request, pk=None):
        # Validate owner
        user = request.user 
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        if task.user != user:
            return HttpResponseForbidden()

        serializer = TaskSerializer(task)
        return Response(ApiResponse.Success(serializer.data))
    
    def create(self, request):  

        user = request.user 
        data = request.data    

        if 'description' not in data or not data['description'].strip():
            return Response(ApiResponse.Error("Description is required"), status=500)
        
        if 'completed' not in data:
            return Response(ApiResponse.Error("Completed is required"), status=500)

        data['user'] = user.id                    
        serializer = TaskSerializer(data=data)

        # When is an update
        if 'id' in data and data['id'] > 0:           

            # Validate owner and existence
            queryset = Task.objects.all()
            task = get_object_or_404(queryset, pk=data['id'])    
            if task.user != user:
                return HttpResponseForbidden()
            task.description = data['description']
            task.completed = data['completed']
            task.save()
            serializer = TaskSerializer(task)
            return Response(ApiResponse.Success(serializer.data))
    

        # When is an creation
        else:
            if serializer.is_valid():
                serializer.save()

        return Response(ApiResponse.Success(serializer.data))

    def delete(self, request, pk, format=None):

        # Validate owner
        user = request.user 
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        if task.user != user:
            return HttpResponseForbidden()

        # Do deletion
        task.delete()
        return Response(ApiResponse.Success("Taks deleted successfully."))        

    @action(detail=True, methods=['post'])
    def mark_as_completed(self, request, pk=None):
        user = request.user 
        data = request.data 
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        if task.user != user:
            return HttpResponseForbidden()
        if 'completed' not in data:
            return Response(ApiResponse.Error("Completed is required"), status=500)
        task.completed = data['completed']
        task.save()        
        return Response(ApiResponse.Success(True))