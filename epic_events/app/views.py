from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, Client, Contract, Event
from .serializers import UserSerializer, ClientSerializer, ContractSerializer, EventSerializer


class UserRegistrationView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @staticmethod
    def create(request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create_user(email=request.data['email'],
                                   last_name=request.data['last_name'],
                                   password=request.data['password'],
                                   first_name=request.data['first_name'],
                                   role=request.data['role'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ClientView(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    @staticmethod
    def create(request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role == 'sales':
                client = serializer.save(sales=request.user)
                client.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                message = 'Only sales users can create clients'
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @staticmethod
    def list(request, *args, **kwargs):
        instances = Client.objects.all()
        serializer = ClientSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientUniqueView(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def info(self, request, *args, **kwargs):
        obj = get_object_or_404(Client, id=kwargs['client_id'])
        serializer = ClientSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Client, id=kwargs['client_id'])
        instance = Client.objects.get(id=kwargs['client_id'])
        serializer = ClientSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(Client, id=kwargs['client_id'])
        self.perform_destroy(obj)
        message = 'You deleted the client'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)


class ContractsView(ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        instances = Contract.objects.all()
        serializer = ContractSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role == "sales":
                contract = serializer.save(sales=request.user)
                contract.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                message = str("Only sales users can create contract")
                return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractUniqueView(ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Contract, id=kwargs['contract_id'])
        serializer = ContractSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Contract, id=kwargs['contract_id'])
        instance = Contract.objects.get(id=kwargs['contract_id'])
        serializer = ContractSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, ** kwargs):
        obj = get_object_or_404(Contract, id=kwargs['contract_id'])
        self.perform_destroy(obj)
        message = 'You deleted the contract'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)


class EventsView(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        instances = Event.objects.all()
        serializer = EventSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role == "support":
                event = serializer.save(support=request.user)
                event.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                message = str("Only support users can create event")
                return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventUniqueView(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Event, id=kwargs['event_id'])
        serializer = EventSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Event, id=kwargs['event_id'])
        instance = Event.objects.get(id=kwargs['event_id'])
        serializer = EventSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, ** kwargs):
        obj = get_object_or_404(Event, id=kwargs['event_id'])
        self.perform_destroy(obj)
        message = 'You deleted the event'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)
