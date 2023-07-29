from django.apps import AppConfig

from MovieReviewAnalyser.predictor import *


class MoviereviewanalyserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MovieReviewAnalyser'

    def ready(self):
        # Initialize your classes here
        self.processor = Processor()
        self.model = Model()
