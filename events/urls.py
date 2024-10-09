from django.urls import path, re_path
from events.views import TransferView

urlpatterns = [
    re_path(r"transfers/(?P<token_id>[0-9]+)", TransferView.as_view(), name="transfers"),
]