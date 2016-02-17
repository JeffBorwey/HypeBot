from imgurpython import ImgurClient as IC


class ImgurClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client = IC(client_id, client_secret)

    # Returns a url to the file
    def upload_file(self, file_name):
        image = self.client.upload_from_path(file_name)
        return image['link']
