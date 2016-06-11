from cloudinary import uploader

class Cloudinary(object):
    def __init__(self, application):
        credentials = application.config['CLOUDINARY_URL'].split('://')[1]
        credentials = credentials.replace("@", ":")
        self.api_key, self.api_secret, self.name = credentials.split(":")

    def upload_image(self, image):
        res = uploader.upload(
            image,
            public_id="profile",
            api_key=self.api_key,
            api_secret=self.api_secret,
            cloud_name=self.name,
        )
        return res['url']

    def compose_url(self, url, size):
        return url
