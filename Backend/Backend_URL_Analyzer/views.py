from rest_framework import viewsets, status
from rest_framework.response import Response

from .URL_model.predict import predict
from .models import URLCheck
from .serializers import URLCheckSerializer


class URLCheckViewSet(viewsets.ModelViewSet):
    queryset = URLCheck.objects.all().order_by('-id')
    serializer_class = URLCheckSerializer

    def create(self, request, *args, **kwargs):
        url = request.data.get('url', " ")
        if not url:
            Response({"error": "Missing URL"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            verdict = predict(url)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        url_check = URLCheck.objects.create(url=url, verdict=verdict)
        output_serializer = self.get_serializer(url_check)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
