from minio import Minio
from django.core.files.uploadedfile import InMemoryUploadedFile
from minio.error import S3Error
import logging

logger = logging.getLogger(__name__)

class MinioStorage:
    def __init__(self, endpoint, access_key, secret_key, secure, ):
        self._client = Minio(endpoint=endpoint,
                             access_key=access_key,
                             secret_key=secret_key,
                             secure=secure)

    def load_file(self, bucket_name: str, file_name: str, file: InMemoryUploadedFile):
        """
        Загрузка файла 'file' с именем 'file_name' в бакет 'bucket_name'
        """
        try:
            self._client.put_object(bucket_name, file_name, file, file.size)
            logger.info(f"Файл {file_name} успешно загружен в бакет {bucket_name}")
        except S3Error as e:
            logger.error(f"Ошибка загрузки файла {file_name} в бакет {bucket_name}: {e}")
            raise

    def delete_file(self, bucket_name: str, file_name: str):
        """
        Удаление файла с именем 'file_name' из бакета 'bucket_name'
        """
        try:
            # Проверка существования файла
            if self._client.stat_object(bucket_name, file_name):
                self._client.remove_object(bucket_name, file_name)
                logger.info(f"Файл {file_name} успешно удален из бакета {bucket_name}")
            else:
                logger.warning(f"Файл {file_name} не существует в бакете {bucket_name}")
        except S3Error as e:
            logger.error(f"Ошибка удаления файла {file_name} из бакета {bucket_name}: {e}")
            raise