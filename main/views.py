from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import CmsUser, Content
from main.filters import ContentFilter
from main.serializers import ContentSerializer, CmsUserSerializer
from rest_framework import generics, permissions, status
from rest_framework.views import APIView 
from rest_framework.decorators import api_view, permission_classes

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.db.models import Q



# Create your views here.
@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'Register':{'url': 'cms/register', 'method':'POST'},
		'Login':{'url': 'cms/login', 'method':'POST'},
		'Create Content':{'url': 'cms/create_content', 'method':'POST'},
		'Update Content':{'url': 'cms/edit_content/<str:pk>', 'method':'POST'},
		'View Content':{'url': 'cms/view_content/<str:pk>', 'method':'GET'},
		'Delete Content':{'url': 'cms/delete_content/<str:pk>', 'method':'DELETE'},
		'Search Content':{'url': 'cms/search_content?quere=<str:query>', 'method':'GET'},
		}

	return Response(api_urls)

@permission_classes([AllowAny])
class RegisterUser(APIView):
    def post(self, request):
        serializers = CmsUserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

# permission_classes([AllowAny])
class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        # print("Request data:", request.data)
        email = request.data.get('email')
        password = request.data.get('password')

        # print(email, password)
        user = authenticate(request, email=email, password=password)
        if user:
            # If the user is successfully authenticated, generate or retrieve a token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.pk})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateContent(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request, *args, **kwargs):

		request.data._mutable = True

		data = request.data
		data['user'] = request.user.id

		serializer = ContentSerializer(data=data)
		
		# Automatically set the user to the currently authenticated user
		if serializer.is_valid():
			
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EditContent(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request, pk):
		content = None
		try:
			content = Content.objects.get(id=pk)
			if not (content.user == request.user or request.user.is_superuser):
				return Response("You cannot edit content not created by you.", status=401)
			# content = Content.objects.get(
			# 	Q(id=pk) &
			# 	Q(
			# 		Q(user=request.user) |
			# 		Q(user=request.user.is_superuser)
			# 	)
			# )
		except Exception as e:
			return Response("Content not found.", status=404)

		data = request.data

		if request.user.is_superuser:
			data['user'] = content.user.id
		else:
			data['user'] = request.user.id

		serializer = ContentSerializer(instance=content, data=data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)


class ViewContent(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request, pk):
		content = None
		try:
			content = Content.objects.get(id=pk)
			if not (content.user == request.user or request.user.is_superuser):
				return Response("You cannot View content not created by you.", status=401)
			
		except Exception as e:
			return Response("Content Not found.", status=401)
		
		serializer = ContentSerializer(instance=content)

		if serializer:
			return Response(serializer.data)
		else:
			return Response({"error": "Something went wrong"}, status=400)

class DeleteContent(APIView):
	permission_classes = [IsAuthenticated]
	def delete(self, request, pk):
		content = None
		try:
			content = Content.objects.get(id=pk)
			if not (content.user == request.user or request.user.is_superuser):
				return Response("You cannot View content not created by you.", status=401)
			
		except Exception as e:
			return Response("You cannot edit content not created by you.", status=401)
		
		content.delete()

		return Response('Content succsesfully deleted !')


class SearchContent(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		query = request.GET.get("query", "")


		queryset = Content.objects.filter(
			Q(title__icontains=query) |
			Q(body__icontains=query) |
			Q(summary__icontains=query) |
			Q(category__icontains=query) 
		)

		if not request.user.is_superuser:
			queryset = queryset.filter(Q(user=request.user))

		serializer = ContentSerializer(queryset, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)
	


		
