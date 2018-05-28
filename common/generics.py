from rest_framework.views import APIView
from rest_framework import status

from .response import Response


class CreateWithStatusAPIView(APIView):
    """Create with status api view"""

    include_data_in_response = False
    serializer_class = None
    status_code = status.HTTP_200_OK

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        response = Response(status=self.status_code)

        if self.include_data_in_response:
            response = Response(
                data=serializer.data,
                status=self.status_code
            )

        return response
