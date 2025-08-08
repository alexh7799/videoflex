from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class VideoView(APIView):
    """_summary_
    VideoView is a view that handles video-related requests.
    Returns:
        _type_: _description_
    """
    permission_classes = [IsAuthenticated]

