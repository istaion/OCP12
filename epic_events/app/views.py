from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, Client, Contract, Event
from .serializers import UserSerializer, ClientSerializer, ContractSerializer, EventSerializer
from .permissions import HasClientPermissions, HasContractPermissions, HasEventPermissions


class UserRegistrationView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @staticmethod
    def create(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            last_name = None
            if "last_name" in request.data:
                last_name = request.data["last_name"]
            first_name = None
            if "first_name" in request.data:
                first_name = request.data["first_name"]
            serializer.create_user(email=request.data["email"],
                                   last_name=last_name,
                                   password=request.data["password"],
                                   first_name=first_name,
                                   role=request.data["role"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ClientView(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, HasClientPermissions]

    @staticmethod
    def create(request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save(sales=request.user)
            client.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        if request.user.role == "support":
            instances = Client.objects.filter(contract__event__support=self.request.user)
        else:
            instances = Client.objects.all()
        serializer = ClientSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(Client, id=pk)
        self.check_object_permissions(self.request, obj)
        serializer = ClientSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        obj = get_object_or_404(Client, id=pk)
        self.check_object_permissions(self.request, obj)
        instance = Client.objects.get(id=pk)
        serializer = ClientSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        obj = get_object_or_404(Client, id=pk)
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = "You deleted the client"
        return Response({"message": message},
                        status=status.HTTP_204_NO_CONTENT)


class ContractsView(ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, HasContractPermissions]

    def list(self, request):
        if request.user.role == "support":
            instances = Contract.objects.filter(event__support=self.request.user)
        else:
            instances = Contract.objects.all()
        serializer = ContractSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            contract = serializer.save(sales=request.user)
            contract.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(Contract, id=pk)
        serializer = ContractSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        obj = get_object_or_404(Contract, id=pk)
        self.check_object_permissions(self.request, obj)
        instance = Contract.objects.get(id=pk)
        serializer = ContractSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        obj = get_object_or_404(Contract, id=pk)
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = "You deleted the contract"
        return Response({"message": message},
                        status=status.HTTP_204_NO_CONTENT)


class EventsView(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, HasEventPermissions]

    def list(self, request, *args, **kwargs):
        instances = Event.objects.all()
        serializer = EventSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data["contract"].signed:
                event = serializer.save()
                event.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                message = str("The contract must be signed to create event")
                return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(Event, id=pk)
        serializer = EventSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        obj = get_object_or_404(Event, id=pk)
        self.check_object_permissions(self.request, obj)
        instance = Event.objects.get(id=pk)
        serializer = EventSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        obj = get_object_or_404(Event, id=pk)
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = "You deleted the event"
        return Response({"message": message},
                        status=status.HTTP_204_NO_CONTENT)
