from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import Client, MailingList, Message
from .scheduler import get_job, pause_job, remove_job, resume_job
from .sendler import send_message
from .serializers import (ClientSerializers, MailingSerializers,
                          MessageSerializers, SendMessageSerializers)


# CLIENTS
class ClientsAPI(ListAPIView):
    """ Возвращает список клиентов."""
    serializer_class = ClientSerializers
    queryset = Client.objects.all()

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializers(clients, many=True)
        return Response(serializer.data)


class ClientCreateAPI(GenericAPIView, CreateModelMixin):
    """ Создаёт клиента в базе данных."""
    serializer_class = ClientSerializers

    def post(self, request):
        serializer = ClientSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientUpdateAPI(GenericAPIView, UpdateModelMixin):
    """ Обновляет данные клиента в базе данных."""
    serializer_class = ClientSerializers
    queryset = Client.objects.all()

    def patch(self, request, pk):
        try:
            instance = Client.objects.get(id=pk)
            serializer = ClientSerializers(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                    )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': 'FAIL',
                    'message': 'Такого клиента нет'
                },
                status=status.HTTP_400_BAD_REQUEST
                )


class ClientDeleteAPI(GenericAPIView, DestroyModelMixin):
    """ Удаляет клиента из базы данных."""
    serializer_class = ClientSerializers
    queryset = Client.objects.all()

    def delete(self, request, pk):
        try:
            Client.objects.get(id=pk).delete()
            return Response(
                {
                    'status': 'SUCCESS',
                    'message': 'Клиент удален.',
                },
                status=status.HTTP_200_OK
                )
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': 'FAIL',
                    'message': 'Такого клиента нет.'
                },
                status=status.HTTP_400_BAD_REQUEST
                )


# MAILING
class MailingListAPI(ListAPIView, ListModelMixin):
    """ Возвращает отфильтрованный список рассылок. \
        Если фильтры не указаны, возвращает весь список рассылок."""
    serializer_class = MailingSerializers
    queryset = MailingList.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['client_operator', 'client_tag']

    def get(self, request, *args, **kwargs):
        queryset = MailingList.objects.all()
        filtered_qs = self.filter_queryset(queryset)
        serializer = MailingSerializers(filtered_qs, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class MailingCreateAPI(GenericAPIView, CreateModelMixin):
    """ Создаёт рассылку"""
    serializer_class = MailingSerializers
    queryset = MailingList.objects.all()

    def post(self, request):
        serializer = MailingSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )


class MailingAPI(GenericAPIView, RetrieveModelMixin):
    """ Возвращает детальную статистику \
        отправленных сообщений по конкретной рассылке"""
    serializer_class = MailingSerializers
    queryset = MailingList.objects.all()

    def get(self, request, pk):
        try:
            context = {}
            messages = Message.objects.filter(mailing_list=pk)
            success_msgs = messages.filter(status='OK')
            context['total_messages_quantity'] = len(messages)
            context['success_messages'] = {
                'quantity': len(success_msgs),
                'messages': MessageSerializers(success_msgs, many=True).data
            }
            fail_msgs = messages.exclude(status='OK')
            context['fail_messages'] = {
                'quantity': len(fail_msgs),
                'messages': MessageSerializers(fail_msgs, many=True).data
            }
            serializer = MailingSerializers(MailingList.objects.get(id=pk))
            context['info'] = serializer.data
            return Response(context, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(
                {
                    'status': 'FAIL',
                    'message': 'Такой рассылки нет.'
                },
                status=status.HTTP_400_BAD_REQUEST
                )


class MailingInfoAPI(ListAPIView, ListModelMixin):
    """ Возвращает общую статистику по всем рассылкам."""
    serializer_class = MailingSerializers
    queryset = MailingList.objects.all()

    def get(self, request):
        context = {}
        messages = Message.objects.all()
        mailing_lists = MailingList.objects.all()
        context['total_message_quantity'] = len(messages)
        context['total_mailing_list_quantity'] = len(mailing_lists)
        context['total_success_messages'] = len(messages.filter(status="OK"))
        context['total_fail_messages'] = len(messages.exclude(status="OK"))
        return Response(context)


class MailingUpdateAPI(GenericAPIView, UpdateModelMixin):
    """ Обновляет параметры рассылки."""
    serializer_class = MailingSerializers
    queryset = MailingList.objects.all()

    def patch(self, request, job_id):
        try:
            instance = MailingList.objects.get(job_id=job_id)
            serializer = MailingSerializers(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                    )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': 'FAIL',
                    'message': 'Такой рассылки нет.'
                },
                status=status.HTTP_400_BAD_REQUEST
                )


class MailingDeleteAPI(GenericAPIView, DestroyModelMixin):
    """ Удалить рассылку."""
    serializer_class = MailingSerializers
    queryset = MailingList.objects.all()

    def delete(self, request, pk):
        try:
            if MailingList.objects.get(id=pk).job_id and \
                    get_job(MailingList.objects.get(id=pk).job_id):
                remove_job(MailingList.objects.get(id=pk).job_id)
            MailingList.objects.get(id=pk).delete()

            return Response(
                {
                    'status': 'SUCCESS',
                    'message': 'Рассылка удалена.',
                },
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': 'FAIL',
                    'message': 'Такой рассылки нет.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class MailingPauseAPI(GenericAPIView, DestroyModelMixin):
    """ Остановить рассылку."""
    serializer_class = MailingSerializers
    queryset = MailingList.objects.all()

    def get(self, request, pk):
        try:
            if MailingList.objects.get(id=pk).job_id and \
                    get_job(MailingList.objects.get(id=pk).job_id):
                pause_job(MailingList.objects.get(id=pk).job_id)
            return Response(
                {
                    'status': 'SUCCESS',
                    'message': 'Рассылка остановлена.',
                },
                status=status.HTTP_200_OK
                )
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': 'FAIL',
                    'message': 'Такой рассылки нет.'
                },
                status=status.HTTP_400_BAD_REQUEST
                )


class MailingResumeAPI(GenericAPIView, DestroyModelMixin):
    """ Возобновить рассылку."""
    serializer_class = MailingSerializers
    queryset = MailingList.objects.all()

    def get(self, request, pk):
        try:
            if MailingList.objects.get(id=pk).job_id and \
                    get_job(MailingList.objects.get(id=pk).job_id):
                resume_job(MailingList.objects.get(id=pk).job_id)
            return Response(
                {
                    'status': 'SUCCESS',
                    'message': 'Рассылка возобновлена.',
                },
                status=status.HTTP_200_OK
                )
        except ObjectDoesNotExist:
            return Response(
                {
                    'status': 'FAIL',
                    'message': 'Такой рассылки нет.',
                },
                status=status.HTTP_400_BAD_REQUEST
                )


# MESSAGES
class MessageAPI(ListAPIView):
    """ Возвращает список всех сообщений."""
    serializer_class = MessageSerializers
    queryset = Message.objects.all()

    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializers(messages, many=True)
        return Response(serializer.data)


# SEND_MESSAGE_TO_CLIENT
class SendMessageAPI(GenericAPIView, CreateModelMixin):
    """ Отправляет сообщение клиенту по указанному номеру. \
        Работает только для клиентов в базе данных."""
    serializer_class = MessageSerializers
    queryset = Message.objects.all()

    def post(self, request):
        serializer = MessageSerializers(data=request.data)
        if serializer.is_valid():
            try:
                message = Message.objects.create(
                    customer=Client.objects.get(
                        phone=str(
                            serializer.data['client_phone']
                            )),
                    send_time=timezone.now(),
                    message=serializer.data['message'],
                )
                send_msg = send_message(
                    message.id,
                    serializer.data['client_phone'],
                    serializer.data['message']
                    )
                message.status = send_msg['message']
                message.save()
                del serializer.data['client_phone']
                return Response(
                    SendMessageSerializers(message).data,
                    status=status.HTTP_201_CREATED
                    )
            except ObjectDoesNotExist:
                return Response(
                    {
                        'status': 'FAIL',
                        'message': 'Такого клиента нет.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
