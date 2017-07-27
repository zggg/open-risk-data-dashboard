# views.py
from datetime import datetime
import json
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from django.db.models import Q
from django.contrib.auth.models import User

from .serializers import (
    RegionSerializer, CountrySerializer,
    ProfileSerializer, UserSerializer, RegistrationSerializer,
    ChangePasswordSerializer,
    ProfileDatasetListSerializer, ProfileDatasetCreateSerializer,
    DatasetListSerializer, DatasetPutSerializer)
from .models import Region, Country, OptIn, Dataset, KeyDataset
from ordd_api import __VERSION__


class VersionGet(APIView):
    """This class handles the GET requests of our rest api."""

    def get(self, request):
        return Response(__VERSION__)


class ProfileDetails(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


class ProfilePasswordUpdate(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def get(self, request, *args, **kwargs):
        # here all the logic to manage the registration confermation
        # - check if user exists and is disabled
        # - check if OptIn record exists
        # - check key against username is correct
        # - turn on user
        # - remove optin row
        # - return success
        # in the other cases return a generic error for security reason

        detail = "user not exists, is already activated or passed key is wrong"
        print("Request GET: username [%s] key [%s]" % (request.GET['username'],
              request.GET['key']))
        user = User.objects.filter(username=request.GET['username'])

        if len(user) != 1:
            raise NotFound(detail)
        user = user[0]

        if user.is_active is True:
            raise NotFound(detail)

        optin = OptIn.objects.filter(user=user)
        if len(optin) != 1:
            raise NotFound(detail)
        optin = optin[0]

        if optin.key != request.GET['key']:
            raise NotFound(detail)

        user.is_active = True
        user.save()

        optin.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RegionListView(generics.ListAPIView):
    """This class handles the GET and POSt requests of our rest api."""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class CountryListView(generics.ListAPIView):
    """This class handles the GET and POSt requests of our rest api."""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailsView(generics.RetrieveAPIView):
    """This class handles the GET and POSt requests of our rest api."""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UserCreateView(generics.ListCreateAPIView):
    """This class handles the GET and POSt requests of our rest api."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles GET, PUT, PATCH and DELETE requests."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class ProfileDatasetListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsOwner, )

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            return ProfileDatasetListSerializer
        elif self.request.method == "POST":
            return ProfileDatasetCreateSerializer

    def get_queryset(self):
        return Dataset.objects.filter(
            owner=self.request.user)

    def perform_create(self, serializer):
        print("perform_create: BEGIN")
        serializer.save(owner=self.request.user, changed_by=self.request.user)


class ProfileDatasetDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileDatasetListSerializer
    permission_classes = (IsOwner, )

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            return ProfileDatasetListSerializer
        else:
            return ProfileDatasetCreateSerializer

    def get_queryset(self):
        return Dataset.objects.filter(
            owner=self.request.user)


class DatasetDetailsViewPerms(permissions.BasePermission):
    """
    Custom permission to only allow members of 'reviewer' and 'admin' groups
    to manage datasets.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            perms = (request.user.groups.filter(name='reviewer').exists() or
                     request.user.groups.filter(name='admin').exists())
        return perms

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            perms = (request.user.groups.filter(name='reviewer').exists() or
                     request.user.groups.filter(name='admin').exists())
        return perms


class DatasetDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the GET requests of our rest api."""
    permission_classes = (DatasetDetailsViewPerms, )
    queryset = Dataset.objects.all()
    serializer_class = DatasetListSerializer

    def get_serializer_class(self):
        try:
            if self.request.method == 'PUT':
                return DatasetPutSerializer
        except:
            pass
        return DatasetListSerializer

    def perform_update(self, serializer):
        # to take a picture of the field before update we follow
        # a serialize->render->deserialize approach
        pre = DatasetPutSerializer(self.get_object())
        pre_json = JSONRenderer().render(pre.data)
        pre = DatasetPutSerializer(data=json.loads(pre_json.decode()))
        pre.is_valid()

        # comodity keydataset is retrieved in a custom way
        pre_keydataset = KeyDataset.objects.get(
            code=pre['keydataset'].value).__str__()

        # update fields
        serializer.validated_data['changed_by'] = self.request.user
        if (pre.validated_data['is_reviewed'] is False and
                serializer.validated_data['is_reviewed'] is True):
            serializer.validated_data['review_date'] = datetime.now()

        # save and get update version of the record
        post = DatasetPutSerializer(serializer.save())
        post_json = JSONRenderer().render(post.data)
        post = DatasetPutSerializer(data=json.loads(post_json.decode()))
        post.is_valid()
        post_keydataset = KeyDataset.objects.get(
            code=post['keydataset'].value).__str__()

        # extract list of read/write field
        if post.Meta.fields == '__all__':
            fields = ()
            for field in post.get_fields():
                if post.Meta.read_only_fields:
                    if field not in post.Meta.read_only_fields:
                        fields += (field,)
                else:
                    fields += (field,)
        else:
            fields = ()
            for field in post.get_fields():
                if field in post.Meta.fields:
                    fields += (field)

        # manage differences between pre and post changes
        for field in fields:
            if field == "keydataset":
                if pre_keydataset != post_keydataset:
                    print("[%s] are different: [%s] => [%s]" % (
                        field, pre_keydataset, post_keydataset))
                else:
                    print("[%s] are identical" % field)
            else:
                if pre[field].value != post[field].value:
                    print("[%s] are different: [%s] => [%s]" % (
                        field, pre[field].value, post[field].value))
                else:
                    print("[%s] are identical" % field)

    def perform_destroy(self, instance):
        print("perform_destroy: BEGIN")
        instance.delete()


class DatasetListView(generics.ListAPIView):
    serializer_class = DatasetListSerializer

    def get_queryset(self):
        queryset = Dataset.objects.all()
        kd = self.request.query_params.getlist('kd')
        country = self.request.query_params.getlist('country')
        category = self.request.query_params.getlist('category')
        applicability = self.request.query_params.getlist('applicability')
        tag = self.request.query_params.getlist('tag')
        is_reviewed = self.request.query_params.getlist('is_reviewed')

        q = Q()
        for v in is_reviewed:
            q = q | Q(is_reviewed__iexact=v)
        queryset = queryset.filter(q)

        q = Q()
        for v in country:
            q = q | Q(country__iso2__iexact=v)
        queryset = queryset.filter(q)

        q = Q()
        for v in kd:
            q = q | Q(keydataset__code__iexact=v)
        queryset = queryset.filter(q)

        q = Q()
        for v in category:
            q = q | Q(keydataset__category__name__iexact=v)
        queryset = queryset.filter(q)

        q = Q()
        for v in applicability:
            # FIXME currently in tag we may have extra applicabilities
            # when category (tag group) is 'hazard'
            q = q | (Q(keydataset__applicability__name__iexact=v) |
                     Q(tag__name__iexact=v))
        queryset = queryset.filter(q)

        q = Q()
        for v in tag:
            q = q | Q(tag__name__iexact=v)
        queryset = queryset.filter(q)

        return queryset
