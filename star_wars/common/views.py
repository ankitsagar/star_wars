# DRF
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

# App
from users.services import UserService


class BaseUserMetaDataListView(ListAPIView):
    serializer_class = None
    model_service_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.model_service = self.model_service_class()

    def list(self, request, user_id, *args, **kwargs):
        query = request.query_params.get('query')
        # Validate given user id is correct
        user = self.user_service.get_by_id(user_id)
        if not user:
            raise NotFound(detail="user id not found")
        queryset = self.model_service.get_model_with_user_metadata_entries(
            user=user, query=query)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return response


class BaseUserMetaDataCreateView(UpdateAPIView):
    serializer_class = None
    model_service_class = None
    not_found_error = None
    instance_context_key = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_service = self.model_service_class()

    def put(self, request, pk, *args, **kwargs):
        instance = self.model_service.get_by_id(pk)
        if not instance:
            raise NotFound(detail=self.not_found_error)

        serializer = self.serializer_class(
            data=request.data,
            context={self.instance_context_key: instance}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
