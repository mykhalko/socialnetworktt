from django.db import transaction
from rest_framework import status
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer
from .permission import ReadOnly, IsPostOwnerOrStaff, LikeActions
from .actions import ACTIONS


class PostListAPIView(APIView, PageNumberPagination, mixins.ListModelMixin):

    permission_classes = IsAuthenticatedOrReadOnly,
    http_method_names = ('get', 'post')

    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset, self.request)

    def get_queryset(self):
        return Post.objects.all()

    def filter_queryset(self, queryset):
        return queryset

    def get_serializer(self, *args, **kwargs):
        return PostSerializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {key: request.data[key] for key in request.data}
        data['author'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostAPIView(APIView, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):

    http_method_names = ('get', 'post','delete')
    queryset = Post.objects.all()
    permission_classes = ReadOnly | IsPostOwnerOrStaff | LikeActions,

    def get_serializer(self, *args, **kwargs):
        return PostSerializer(*args, **kwargs)

    def get_object(self):
        obj = self.queryset.get(id=self.kwargs.get('id'))
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        if 'action' not in request.data:
            errors = {
                'detail': 'no action provided',
                'available_actions': [ACTIONS.keys()]
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        action = request.data.get('action')
        if action in ACTIONS:
            with transaction.atomic():
                obj = self.get_object()
                ACTIONS[action](request.user, obj)
            return Response(status=status.HTTP_200_OK)
        errors = {
            'detail': 'incorrect action',
            'available_actions': [ACTIONS.keys()]
        }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic()
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
