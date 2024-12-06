from osbot_aws.aws.s3.S3__Key_Generator import S3__Key_Generator
from osbot_utils.decorators.methods.type_safe import type_safe
from osbot_utils.helpers.Safe_Id import Safe_Id
from osbot_utils.utils.Misc             import random_guid

S3_FOLDER__PUBLIC_DATA = 'public-data'

class Hacker_News__S3__Key_Generator(S3__Key_Generator):

    @type_safe
    def create(self, area: Safe_Id , file_id: Safe_Id):

        path_elements = [S3_FOLDER__PUBLIC_DATA, area] + self.create_path_elements__from_when()

        s3_key = self.create_s3_key(path_elements=path_elements, file_id=file_id)
        return s3_key

