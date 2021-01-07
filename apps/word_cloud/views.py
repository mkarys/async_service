from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.word_cloud.serializers import KeywordsSerializer, WordCloudSerializer
from apps.word_cloud.utils import create_image_for_words, get_related_words


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

        for word_cloud in word_clouds:
            word_cloud.related_words = get_related_words(word_cloud.keyword)
            word_cloud.image = create_image_for_words(
                word_cloud.keyword, word_cloud.related_words
            )
            word_cloud.save(update_fields=("related_words", "image"))

        return Response(word_cloud_serializer.data, status=status.HTTP_200_OK)
