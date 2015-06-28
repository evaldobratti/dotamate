from django.shortcuts import render

def match_detail(request, match_id):
    return render(request, 'web/match.html')
