
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.test.utils import override_settings
import json

endpoint = "http://127.0.0.1:8000"

class TasksModelTests(TestCase):

    def test_retrieve_tasks_not_logged(self):       

        client = APIClient()                      
        response = client.get(endpoint + '/tasks', format='json')    
                
        assert response.status_code == 401

    def test_retrieve_tasks_logged(self):       

        user = User.objects.create_user('admin', 'admin')
        client = APIClient()              
        client.force_authenticate(user=user)                   
        response = client.get(endpoint + '/tasks', format='json')    
                
        assert response.status_code == 200

    def test_task_creation(self):       

        user = User.objects.create_user('admin', 'admin')
        client = APIClient()              
        client.force_authenticate(user=user)
        response = client.post(endpoint + '/tasks', {
            'description': 'this is a test',
            'completed': True
        }, format='json')    

        assert response.status_code == 200
    
    def test_task_creation_with_description_empty(self):       

        user = User.objects.create_user('admin', 'admin')
        client = APIClient()              
        client.force_authenticate(user=user)
        response = client.post(endpoint + '/tasks', {
            'description': ' ',
            'completed': True
        }, format='json')    

        assert response.status_code == 500 #error
    
    def test_task_creation_with_description_none(self):       
               
        user = User.objects.create_user('admin', 'admin')
        client = APIClient()              
        client.force_authenticate(user=user)
        response = client.post(endpoint + '/tasks', {
            'completed': True
        }, format='json')       
 
        assert response.status_code == 500
    
    def test_task_creation_without_completed(self):       
               
        user = User.objects.create_user('admin', 'admin')
        client = APIClient()              
        client.force_authenticate(user=user)
        response = client.post(endpoint + '/tasks', {
            'description': 'this is a test'            
        }, format='json')    
        
        assert response.status_code == 500
    
    def test_retrive_a_task_does_not_exist(self):       

        user = User.objects.create_user('admin', 'admin')
        client = APIClient()              
        client.force_authenticate(user=user)
        response = client.get(endpoint + '/tasks/15900', format='json')    
        
        assert response.status_code == 404
    
    def test_retrieve_task_fron_another_user(self):       

        user1 = User.objects.create_user('user1', 'user1')
        client1 = APIClient()              
        client1.force_authenticate(user=user1)
        response1 = client1.post(endpoint + '/tasks', {
            'description': 'this is a test',
            'completed': True
        }, format='json')    
        obj = json.loads(response1.content)
        task1Id = obj["data"]["id"]

        user2 = User.objects.create_user('user2', 'user2')
        client2 = APIClient()              
        client2.force_authenticate(user=user2)
        response2 = client2.get(endpoint + '/tasks/' + str(task1Id), format='json')    

        assert response2.status_code == 403
    
    
    def test_mark_task_as_completed(self):       

        user1 = User.objects.create_user('user1', 'user1')
        client1 = APIClient()              
        client1.force_authenticate(user=user1)
        
        response1 = client1.post(endpoint + '/tasks', {
            'description': 'this is a test',
            'completed': False
        }, format='json')    

        obj = json.loads(response1.content)
        task1Id = obj["data"]["id"]

        response2 = client1.post(endpoint + '/tasks/' + str(task1Id) + '/mark_as_completed', {
            "completed": True
        }, format='json') 

        obj2 = json.loads(response2.content)

        assert response2.status_code == 200 and obj2["data"] == True

    def test_mark_task_as_not_completed(self):       

        user1 = User.objects.create_user('user1', 'user1')
        client1 = APIClient()              
        client1.force_authenticate(user=user1)
        
        response1 = client1.post(endpoint + '/tasks', {
            'description': 'this is a test',
            'completed': False
        }, format='json')    

        obj = json.loads(response1.content)
        task1Id = obj["data"]["id"]

        response2 = client1.post(endpoint + '/tasks/' + str(task1Id) + '/mark_as_completed', {
            "completed": False
        }, format='json') 
        
        obj2 = json.loads(response2.content)

        assert response2.status_code == 200 and obj2["data"] == True

    def test_mark_task_as_completed_without_not_completed_param(self):       

        user1 = User.objects.create_user('user1', 'user1')
        client1 = APIClient()              
        client1.force_authenticate(user=user1)
        
        response1 = client1.post(endpoint + '/tasks', {
            'description': 'this is a test',
            'completed': False
        }, format='json')    

        obj = json.loads(response1.content)
        task1Id = obj["data"]["id"]

        response2 = client1.post(endpoint + '/tasks/' + str(task1Id) + '/mark_as_completed', format='json') 
        
        obj2 = json.loads(response2.content)

        assert response2.status_code == 500


    
    
   