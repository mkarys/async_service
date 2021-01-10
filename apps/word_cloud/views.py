from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from time import time

from apps.word_cloud.serializers import KeywordsSerializer, WordCloudSerializer
from apps.word_cloud.utils import run_async, run_sync


class WordCloudView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        keyword_serializer = KeywordsSerializer(data={"keywords": request.data})
        keyword_serializer.is_valid(raise_exception=True)
        keywords = keyword_serializer.data["keywords"]

        keywords_data = [{"keyword": keyword} for keyword in keywords]

        word_cloud_serializer = WordCloudSerializer(
            data=keywords_data, many=True, context={"request": request}
        )
        word_cloud_serializer.is_valid(raise_exception=True)
        word_clouds = word_cloud_serializer.save()

        total_time_start = time()
        for word_cloud in word_clouds:
            time_start = time()
            if settings.ASYNC:
                related_words, image = run_async(word_cloud)
            else:
                related_words, image = run_sync(word_cloud)

            time_taken = time() - time_start

            print(
                f"Used {'async' if settings.ASYNC else 'sync'} function. It took {time_taken} s."
            )

            word_cloud.related_words = related_words
            word_cloud.image = image
            word_cloud.save(update_fields=("related_words", "image"))

        total_time_taken = time() - total_time_start
        print(f"It took in total {total_time_taken} s.")

        return Response(word_cloud_serializer.data, status=status.HTTP_200_OK)
