from django.shortcuts import render
from django.http import HttpResponse
from scraper.skill_scraper import find_best_skills, get_url_list, get_personal_skills, find_related_courses
import requests
import json
import urllib, urllib2
import os
from django.utils.safestring import SafeString
# Create your views here.

client_id = "m70mm27vpve4"
client_secret = "dSP3GwJhL9UZWjGJ"
skills_json = []

profile_api_endpoint = "https://api.linkedin.com/v1/people/~/connections:(public-profile-url)"
own_skills_endpoint = "https://api.linkedin.com/v1/people/~:(skills)"

def auth(request):
    return render(request, "welcome.html")

def get_token(request):
    if request.method == 'GET':
        err = request.GET.get('error', None)
        if err is not None:
            return render(request, "auth_fail.html", {'error': 'wrong linkedin creds'})
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)
        match = "aaa" #TODO: store states in db
        if code is None or state is None or state != match:
            return render(request, "auth_fail.html", {"error": "bad return values"})
        auth_url = "https://www.linkedin.com/uas/oauth2/accessToken"
        data = {
            "grant_type" : "authorization_code",
            "code" : str(code),
            "redirect_uri" : "http://localhost:8000/youarein",
            "client_id" : client_id,
            "client_secret" : client_secret
        }
        post_url = auth_url + "?grant_type={0}&code={1}&redirect_uri={2}&client_id={3}&client_secret={4}".format(data["grant_type"], data["code"], data["redirect_uri"], data["client_id"], data["client_secret"])
        r = requests.post(post_url)
#print auth_url+urllib.urlencode(data)
#r = requests.post(auth_url, data=data)
#r = urllib2.urlopen(auth_url, urllib.urlencode(data))
        if r.status_code != requests.codes.ok:
            print "problem occured getting auth token"
        r = json.loads(r.text)
        token = r.get("access_token", None)
        if token is None:
            return render(request, "auth_fail.html", {"error": "could not acquire token"})
        print "requesting connections data"
        basic_data = requests.get(profile_api_endpoint+"?oauth2_access_token={0}".format(token))
        url_list = get_url_list(basic_data.text)
#print url_list
        print "requesting skills data"
        own_data = requests.get(own_skills_endpoint+"?oauth2_access_token={0}".format(token))
        own_list = get_personal_skills(own_data.text)
#print own_list
        print "processing lists"
        best_list = find_best_skills(url_list, own_list)
        
        best_list = best_list.items()
        best_list.sort(key=lambda(x):x[1],reverse=True)
        skills_json = json.dumps(flarify(best_list))
        final_list = []
        for element in best_list:
            final_list.append(element[0])
        print best_list
        print final_list
        course_list = find_related_courses(final_list)
        print course_list
        
        return render(request, "results.html", {'skill_list': final_list, 'course_list': course_list[:50], 'skills_json': SafeString(skills_json)}) 
    else:
        return render(request, "please_wait.html")

def flarify(tuples):
    children = []
    print "++++++++++++++++++++flarify ++++++++++++++++++++++++++++++++" 
    for i in range(50):
        print tuples[i]
        children.append({"name": tuples[i][0], "size": tuples[i][1]})
    flare_dict = {"name": "flare", "children": children}
    return flare_dict

        
