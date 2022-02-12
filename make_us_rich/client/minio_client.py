from minio import Minio

from make_us_rich.utils import load_env


class MinioClient:

    def __init__(self) -> None:
        """
        Initializes the Minio client.

        Returns
        -------
        None
        """
        self._config = load_env("minio")
        self.client = Minio(
            self._config["ENDPOINT"],
            access_key=self._config["ACCESS_KEY"],
            secret_key=self._config["SECRET_KEY"],
            secure=False
        )
        self.bucket = self._config["BUCKET"]
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
        

    def upload(self, bucket: str, object_name: str, file_path: str) -> None:
        """
        Uploads a file to Minio.

        Parameters
        ----------
        bucket: str
            Bucket name.
        object_name: str
            Object name.
        file_path: str
            File path.

        Returns
        -------
        None
        """
        self.client.fput_object(
            bucket_name=bucket, object_name=object_name, file_path=file_path
        )

    
    def download(self, bucket: str, object_name: str, file_path: str) -> None:
        """
        Downloads a file from Minio.

        Parameters
        ----------
        bucket: str
            Bucket name.
        object_name: str
            Object name.
        file_path: str
            File path.

        Returns
        -------
        None
        """
        self.client.fget_object(
            bucket_name=bucket, object_name=object_name, file_path=file_path
        )
