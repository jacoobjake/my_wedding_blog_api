from rest_framework.response import Response
from guest_list.serializers import GuestSerializer, PhotoSerializer
from guest_list.documents import *
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import renderers
from django.http import Http404
from rest_framework import status
from mongoengine.queryset.visitor import Q
from bson import ObjectId
from rest_framework.exceptions import APIException

class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Record not found!"

# API Root
@api_view(['GET'])
def api_root(request, format=None):
        return Response({
            'guests': reverse('guest-list', request=request, format=format),
            'guests_internal': reverse('guest-list-internal', request=request, format=format),
            'guests_by_details': reverse('guest-by-details', request=request, format=format),
            'photo_list': reverse('photo-list', request=request, format=format),
            'photo_list_internal': reverse('photo-list-internal', request=request, format=format),
            'photo_carousel': reverse('photo-carousel', request=request, format=format),
            'photo_event': reverse('photo-event', request=request, format=format),
        })

# Using View Sets
class PhotoListViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class GuestViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

#     @action(detail=True)
#     def get_by_details(self, request, *args, **kwargs):
#         params = request.query_params
#         if(params.get('keyword') is None):
#             return Response({"detail": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             guest = Guest.objects(Q(email=params['keyword']) | Q(phone=params['keyword'])).get()
#         except Guest.DoesNotExist:
#             # raise Http404
#             return Response({"detail": "Guest not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = GuestSerializer(guest)
#         return Response({"detail": "Guest details retrieved successfully", "data": serializer.data})

    # Custom endpoints
    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     snippet = self.get_object()
    #     return Response(snippet.highlighted)

# Generic API View format
# from rest_framework import mixins
# from rest_framework import generics
# class GuestList(generics.ListCreateAPIView):
#     queryset = Guest.objects.all()
#     serializer_class = GuestSerializer

# class GuestDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Guest.objects.all()
#     serializer_class = GuestSerializer

# Custom API View Format
from rest_framework.views import APIView
class GuestByKeyword(APIView):
    def get(self, request, format=None):
        params = request.query_params
        if(params.get('keyword') is None):
            return Response({"detail": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            guest = Guest.objects(Q(email=params['keyword']) | Q(phone=params['keyword'])).get()
        except Guest.DoesNotExist:
            return Response({"detail": "Guest not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GuestSerializer(guest)
        return Response({"detail": "Guest details retrieved successfully", "data": serializer.data})

class GuestList(APIView):
    def get(self, request, format=None):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response({"detail": "Guest list retrieved successfully", "data": serializer.data})
    def post(self, request, format=None):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Guest created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Error creating guest", "data": {}, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GuestDetail(APIView):
    """
    Retrieve, update or delete a guest instance.
    """
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise NotFoundException

    def get(self, request, pk, format=None):
        if(ObjectId.is_valid(pk) == False):
            return Response({"detail": "Invalid Object Id"}, status=status.HTTP_400_BAD_REQUEST)
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response({"detail": "Guest details retrieved successfully", "data": serializer.data})

    def put(self, request, pk, format=None):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Guest updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"detail": "Error updating guest", "data": {}, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Guest updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"detail": "Error updating guest", "data": {}, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        guest = self.get_object(pk)
        guest.delete()
        return Response({"detail": "Guest deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class PhotoList(APIView):
    def get(self, request, format=None):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response({"detail": "Photo list retrieved successfully", "data": serializer.data})
    def post(self, request, format=None):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Photo created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Error creating Photo", "data": {}, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_carousel(request):
    photos = Photo.objects(is_carousel = True).all()
    serializer = PhotoSerializer(photos, many=True)
    return Response({"detail": "Photo list retrieved successfully", "data": serializer.data})

@api_view(['GET'])
def get_event_cover(request):
    query = Photo.objects(is_event_cover = True)
    if(query.count() < 1):
        return Response({"detail": "Photo not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = PhotoSerializer(query[0])
    return Response({"detail": "Photo retrieved successfully", "data": serializer.data})
