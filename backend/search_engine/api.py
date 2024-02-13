from search_engine.models import People
from rest_framework import viewsets, permissions
from .serializers import PeopleSerializer

# People Viewset
class PeopleViewSet(viewsets.ModelViewSet):
    
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = PeopleSerializer

    #fetches all query sets from our search_engine app
    def get_queryset(self):
        return self.request.user.search_engine.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)