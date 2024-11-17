import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from notes import constants
from notes.serializers import NotesSerializer
from notes.models import Notes
from core.utils.cache import CacheInvalidationMixin


logger = logging.getLogger(__name__)


class NotesListCreateView(APIView, CacheInvalidationMixin):
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(
        operation_summary="POST request",
        operation_description="Create a new Note object",
        request_body=NotesSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Note was created successfully",
                schema=NotesSerializer,
                examples={
                    "id": 1,
                    "title": "New Note",
                    "content": "New Note Content"
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data submission")
        }
    )
    def post(self, request):
        data = request.data
        data['created_by'] = request.user.id

        serializer = NotesSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            self.invalidate_cache(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(
        operation_summary="GET request",
        operation_description="Get the list of all notes for current authenticated user",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="A list of Notes objects",
                schema=NotesSerializer(many=True),
                examples=[
                    {
                        "id": 1,
                        "title": "Note 1",
                        "content": "Note Content 1"
                    },
                    {
                        "id": 2,
                        "title": "Note 2",
                        "content": "Note Content 2"
                    },
                ]
            )
        }
    )
    def get(self, request):
        cache_key = self.notes_cache_key(request.user)
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info('Retrieving Notes from cache for User %s', request.user.id)
            return Response(cached_data, status=status.HTTP_200_OK)

        notes = Notes.objects.filter(created_by=request.user)
        serializer = NotesSerializer(notes, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 15)
        logger.info('Notes cache set for User %s', request.user.id)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
class NotesUpdateDeleteView(APIView, CacheInvalidationMixin):
    permission_classes = [permissions.IsAuthenticated, ]
    
    @swagger_auto_schema(
        operation_summary="PATCH request",
        operation_description="Update the selected Notes instance",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="Notes object ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=NotesSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Note was successfully updated",
                schema=NotesSerializer,
                examples={
                    "id": 1,
                    "title": "Updated Title",
                    "content": "Updated Content"
                }
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(description="Notes object was not found"),
            status.HTTP_403_FORBIDDEN: openapi.Response(description="Edit access was denied"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid data submission")
        }
    )
    def patch(self, request, *args, **kwargs):
        note_id = kwargs.get('id')

        try:
            notes_obj = Notes.objects.get(id=note_id)
        except Notes.DoesNotExist:
            logger.error(constants.NOTE_NOT_FOUND_MESSAGE(note_id))
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.id != notes_obj.created_by.id:
            logger.error(constants.ACCESS_DENIED_FOR_USER('PATCH', request.user.id))
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = NotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(notes_obj, serializer.validated_data)
            self.invalidate_cache(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="DELETE request",
        operation_description="Delete the selected Notes instance",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="Notes object ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description="Notes instance was successfully deleted"),
            status.HTTP_404_NOT_FOUND: openapi.Response(description="Notes object was not found"),
            status.HTTP_403_FORBIDDEN: openapi.Response(description="Edit access was denied"),
        }
    )
    def delete(self, request, *args, **kwargs):
        note_id = kwargs.get('id')

        try:
            notes_obj = Notes.objects.get(id=note_id)
        except Notes.DoesNotExist:
            logger.error(constants.NOTE_NOT_FOUND_MESSAGE(note_id))
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.id != notes_obj.created_by.id:
            logger.error(
                constants.ACCESS_DENIED_FOR_USER('DELETE', request.user.id)
            )
            return Response(status=status.HTTP_403_FORBIDDEN)

        notes_obj.delete()
        self.invalidate_cache(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
