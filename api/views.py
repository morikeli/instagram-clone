from django.shortcuts import render
from rest_framework import generics, response, status
from .serializers import SignupSerializer


class SignupAPIView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return response.Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        
        serializer.save()
        return response.Response({
            "detail": "Account created successfully!", 
            "data": serializer.data}, 
            status=status.HTTP_201_CREATED,
        )



