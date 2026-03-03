import datetime
from datetime import timezone
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .URL_model.predict import predict
from .models import URLCheck
from .serializers import URLCheckSerializer
from .utils import validate_url


class URLCheckPagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 50


class URLCheckViewSet(viewsets.ModelViewSet):
    queryset = URLCheck.objects.all().order_by('-checked_at')
    serializer_class = URLCheckSerializer
    pagination_class = URLCheckPagination

    def create(self, request, *args, **kwargs):
        url = request.data.get('url', " ")
        if not url:
            return Response({"error": "Missing URL"}, status=status.HTTP_400_BAD_REQUEST)
        a = validate_url(url)
        print(a)
        if not a:
            return Response({"error": "Invalid URL"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            verdict = predict(url)
        except Exception:
            return Response({"error": "Error at URL analysis"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url_check = URLCheck.objects.create(url=url, verdict=verdict)
        output_serializer = self.get_serializer(url_check)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "URL deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def reanalyze(self, request, pk=None):
        url_check = self.get_object()
        try:
            verdict = predict(url_check.url)
            url_check.verdict = verdict
            url_check.checked_at = timezone.now()
            url_check.save()
        except Exception:
            return Response({"error": "Error at URL re-analysis"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(url_check)
        return Response(serializer.data)
