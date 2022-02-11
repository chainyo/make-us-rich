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
        