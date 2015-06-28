from django.shortcuts import render
from utils import get_details_match
from rest_framework.response import Response
from rest_framework.decorators import api_view
from serializers import DetailMatchSerializer
from django.db import transaction
# Create your views here.

@api_view(['GET'])
@transaction.atomic()
def match_detail(request, match_id):
    return Response(DetailMatchSerializer(get_details_match(match_id)).data)
