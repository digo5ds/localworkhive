"""AWS Resource helpers to manage resources."""

from io import BytesIO

import boto3

from app.common.constants import LOCALSTACK_ENDPOINT
from app.helpers.exception_mixin import boto_exceptions_handdler
from app.interfaces.aws_resources_interface import ResourcesInterface
from app.schemas.aws_resources_basemodels import SQSMessageBaseModel, SQSQueueBaseModel


class QueueSQS(ResourcesInterface):
    """QueueSQS provides an interface for managing AWS SQS queues using boto3,
    suportando operações como criação, envio, recebimento, deleção e listagem de filas.

    Attributes:
        sqs (boto3.client): O cliente boto3 SQS configurado para o endpoint e região.

    Methods:
        __init__(region_name="us-east-1"):
            Inicializa o cliente SQS.

        new_resource(resource_model):
            Cria uma nova fila SQS.

        delete_resource(resource_model):
            Deleta uma fila SQS.

        list_resources(resource_model=None):
            Lista todas as filas SQS.

        send_message(resource_model, message_body):
            Envia uma mensagem para a fila.

        receive_message(resource_model):
            Recebe mensagens da fila.
    """

    def __init__(self, region_name="us-east-1"):
        self.sqs = boto3.client(
            "sqs",
            endpoint_url=LOCALSTACK_ENDPOINT,
            region_name=region_name,
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )

    @boto_exceptions_handdler
    def new_resource(self, resource_model: SQSQueueBaseModel):
        """Cria uma nova fila SQS.

        Parameters:
        resource_model (SQSQueueBaseModel): O modelo da fila SQS a ser criada.

        Returns:
        str: A URL da fila SQS criada.

        Raises:
        botocore.exceptions.ClientError: Se a operação falhar.
        """
        response = self.sqs.create_queue(QueueName=resource_model.queue_name)
        return response["QueueUrl"]

    @boto_exceptions_handdler
    def delete_resource(self, resource_model):
        """Deleta uma fila SQS.

        Parameters:
        resource_model (SQSQueueBaseModel): O modelo da fila SQS a ser deletada.

        Returns:
        bool: True se a fila for deletada com sucesso.

        Raises:
        botocore.exceptions.ClientError: Se a operação falhar.
        """
        self.sqs.delete_queue(QueueUrl=resource_model.queue_url)
        return True

    @boto_exceptions_handdler
    def list_resources(self, resource_model=None):
        """Lista todas as filas SQS.

        Parameters:
        resource_model (SQSQueueBaseModel): Opcional, o modelo da fila SQS.

        Returns:
        list: A lista de URLs das filas SQS.

        Raises:
        botocore.exceptions.ClientError: Se a operação falhar.
        """
        response = self.sqs.list_queues()
        return response.get("QueueUrls", [])

    @boto_exceptions_handdler
    def send_message(self, resource_model: SQSQueueBaseModel, message_body: str):
        """Envia uma mensagem para uma fila SQS.

        Parameters:
        resource_model (SQSQueueBaseModel): O modelo da fila SQS.
        message_body (str): O conteúdo da mensagem.

        Returns:
        dict: A resposta da SQS.
        """
        response = self.sqs.send_message(
            QueueUrl=resource_model.queue_url,
            MessageBody=message_body,
        )
        return response

    @boto_exceptions_handdler
    def receive_message(self, resource_model: SQSQueueBaseModel, max_number=1):
        """Recebe mensagens de uma fila SQS.

        Parameters:
        resource_model (SQSQueueBaseModel): Modelo da fila SQS.
        max_number (int): N mero m ximo de mensagens a serem recebidas.

        Returns:
        list: Lista de mensagens recebidas.
        """
        response = self.sqs.receive_message(
            QueueUrl=resource_model.queue_url,
            MaxNumberOfMessages=max_number,
        )
        return response.get("Messages", [])
