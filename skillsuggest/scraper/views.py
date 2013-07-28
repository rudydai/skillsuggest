from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import urllib, urllib2
# Create your views here.

client_id = "m70mm27vpve4"
client_secret = "dSP3GwJhL9UZWjGJ"

profile_api_endpoint = "https://api.linkedin.com/v1/people/~/connections:(public-profile-url)"

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
            "redirect_uri" : "http://localhost:8080/youarein",
            "client_id" : client_id,
            "client_secret" : client_secret
        }
        post_url = auth_url + "?grant_type={0}&code={1}&redirect_uri={2}&client_id={3}&client_secret={4}".format(data["grant_type"], data["code"], data["redirect_uri"], data["client_id"], data["client_secret"])
        print post_url
        r = requests.post(post_url)
#print auth_url+urllib.urlencode(data)
#r = requests.post(auth_url, data=data)
#r = urllib2.urlopen(auth_url, urllib.urlencode(data))
        print r
        print r.text
        if r.status_code != requests.codes.ok:
            print "problem occured getting auth token"
        r = json.loads(r.text)
        token = r.get("access_token", None)
        if token is None:
            return render(request, "auth_fail.html", {"error": "could not acquire token"})
        basic_data = requests.get(profile_api_endpoint+"?oauth2_access_token={0}".format(token))
        print basic_data
        print basic_data.text
        return HttpResponse(basic_data.text)
    else:
        return render(request, "please_wait.html")


        
