import requests
import json

actionBGPCommunitiesList = [
  1031,
  65002,
  65003,
  65004,
]

def getRouteServerList():
  response = requests.get('https://lg.ix.br/api/v1/routeservers')
  if response.status_code == 200:
    return json.loads(response.text)
  else:
    return None

def getRouteServerNeighbors(routeServerId):
  response = requests.get('https://lg.ix.br/api/v1/routeservers/'+routeServerId+'/neighbors')
  if response.status_code == 200:
    return json.loads(response.text)
  else:
    return None

def getAnnouncedRoutes(routeServerId, neighborId, page=1):
  # essa funcao deve retornar todos os valores de todas as paginas
  response = requests.get('https://lg.ix.br/api/v1/routeservers/'+routeServerId+'/neighbors/'+neighborId+'/routes/received?page='+str(page)) # TODO: verificar se o query param de page esta correto
  if response.status_code == 200:
    return json.loads(response.text)
  else:
    return None

def getAllActionBGPCommunitties(communitiesList) -> list:
  participatingCommunities = []
  for community in communitiesList:
    if ((community[0] in actionBGPCommunitiesList) and not(community[0] in participatingCommunities)): 
      participatingCommunities.append(community[0])
  return participatingCommunities

def displayInformation(neighborComunityDict):
  for neighbor in neighborComunityDict:
    print('Neighbor ID: ' + neighbor)
    print('Participating Communities: ')
    for community in neighborComunityDict[neighbor]:
      print('  ' + str(community))
    print('')

if __name__ == '__main__':
  routesReceivedJson = json.load(open('routesreceived'))
  
  # totalPages = routesReceivedJson.pagination.total_pages
  # currentPage = 1
  neighbors = routesReceivedJson.get('imported')
  neighborComunityDict = {}
  for neighbor in neighbors:
    communitiesList = list(neighbor.get('bgp').get('communities'))
    # TODO: devo usar só communities ou large communities tambem?
    # largeCommunitiesList = list(neighbor.get('bgp').get('large_communities'))

    neighborComunityDict[neighbor.get('id')] = getAllActionBGPCommunitties(communitiesList) 

  displayInformation(neighborComunityDict)