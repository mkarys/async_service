from rest_framework import serializers

from apps.word_cloud.models import WordCloud


class KeywordsSerializer(serializers.Serializer):
    keywords = serializers.ListField(child=serializers.CharField())


class WordCloudSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = WordCloud
        fields = ("keyword", "related_words", "image")
        extra_kwargs = {
            "related_words": {"write_only": True},
        }

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
