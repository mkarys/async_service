from django.contrib import admin

from apps.word_cloud.models import WordCloud


class WordCloudAdmin(admin.ModelAdmin):
    list_display = ["pk", "keyword", "related_words", "image"]


admin.site.register(WordCloud, WordCloudAdmin)
