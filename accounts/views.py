from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_api_key.permissions import HasAPIKey
from django.views.decorators.csrf import csrf_exempt
from rest_framework_api_key.models import APIKey
import coreapi
from . import datajson
from geopy.distance import distance,lonlat

#Creates the user account. 
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request, format='json'):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            u = serializer.data
            keyname="remote-access-key"+str(u['id'])
            api_key, key = APIKey.objects.create_key(name=keyname)
            Token.objects.get_or_create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#login with username and pwd
@permission_classes((AllowAny,))
@api_view(['POST'])
def login(request, format='json'):
    data=request.data
    if data['username'] is None or data['password'] is None:
        return Response({'error': 'username ou password non defini'},status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=data['username'],password=data['password'])
    if user is not None:
        token= Token.objects.get(user=user)
        return Response({"token":token.key}, status=status.HTTP_202_ACCEPTED)
    return Response('Verifier les identifiants', status=status.HTTP_404_NOT_FOUND)

#get api keys
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getkeys(request):
    api_key = APIKey.objects.get_from_key('remote-access-key')
    return Response(str(api_key))

#restaurents list
@api_view(['POST'])
@permission_classes((HasAPIKey,))
def getNearbyRestautants(request):
    client = coreapi.Client()
    schema = client.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json')
    data = request.data
    location = (data['lat'],data['lng'])
    radius = 3000
    placetype = 'restaurant'
    key = ''
    params = {"location": location, "radius": radius,"type":placetype,"key":key}
    #result = client.action(schema, [], params)
    results = datajson.data['results']
    toreturn = []
    for place in results:
        obj = {}
        obj['location'] = place['geometry']['location']
        obj['name'] = place['name']
        obj['place_id'] = place['place_id']
        ecart = distance(
            lonlat(
            *(data['lng'],data['lat'])
         ),
         lonlat(
            *(place['geometry']['location']['lng'],place['geometry']['location']['lat'])
         )
        )
        obj['distance'] = ecart.miles
        toreturn.append(obj)
    return Response(toreturn)