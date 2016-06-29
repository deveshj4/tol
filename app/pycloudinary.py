from cloudinary import uploader, CloudinaryImage, config

class Cloudinary(object):
    def __init__(self, application):
        credentials = application.config['CLOUDINARY_URL'].split('://')[1]
        credentials = credentials.replace("@", ":")
        self.api_key, self.api_secret, self.name = credentials.split(":")
        config(
              cloud_name = self.name,
              api_key = self.api_key,
              api_secret = self.api_secret
        )

    def upload_image(self, image, public_id):
        res = uploader.upload(
            image,
            public_id=public_id
        )
        return res['url']

    def compose_url(self, name, width, height):
        return CloudinaryImage(name).build_url(width=width, height=height,
                                               crop="fit")
