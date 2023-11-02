import requests
import json

# Lista de Comunidades de Ação BGP
# TODO: atualizar com os valores corretos
actionBGPCommunitiesList = [
  65002,
  65003,
  65004,
]

# Retorna a lista de todos os servidores
def getRouteServerList() -> list:
  response = requests.get('https://lg.ix.br/api/v1/routeservers')
  if response.status_code == 200:
    return list(json.loads(response.text).get('routeservers'))
  else:
    return None

# Retorna os neighbors do serverId
def getRouteServerNeighbors(serverId) -> list:
  response = requests.get('https://lg.ix.br/api/v1/routeservers/'+serverId+'/neighbors')
  if response.status_code == 200:
    return list(json.loads(response.text).get('neighbors'))
  else:
    return None

# Retorna as rotas anunciadas pelo neighborId (na pagina especificada)
def getAnnouncedRoutes(serverId, neighborId, page):
  response = requests.get('https://lg.ix.br/api/v1/routeservers/'+serverId+'/neighbors/'+neighborId+'/routes/received?page='+str(page))
  return json.loads(response.text)

# Função usada para fazer a paginação das rotas anunciadas.
# Retorna uma lista com todas as rotas anunciadas pelo neighborId
def getAllAnnouncedRoutesOfNeighbor(serverId, neighborId) -> list:
  allRoutes = []
  currentPage = 0
  while True:
    announcedRoutes = getAnnouncedRoutes(serverId, neighborId, currentPage)
    currentPage += 1

    allRoutes += list(announcedRoutes.get('imported'))

    ## Condições de saída
    # se for a ultima pagina
    if announcedRoutes.get('pagination').get('total_pages') - 1 == currentPage: break
    # se o campo 'imported' estiver vazio
    if not(announcedRoutes.get('imported')): break
    # se der problema no loop, sai na centesima pagina
    if currentPage == 100 : break

  return allRoutes

# Retorna uma lista com todas as rotas anunciadas por um servidor
def getAllAnnouncedRoutesOfServer(serverId) -> list:
  allRoutes = []
  neighbors = getRouteServerNeighbors(serverId)
  counter = 0
  for neighbor in neighbors:
    allRoutes += getAllAnnouncedRoutesOfNeighbor(serverId, neighbor.get('id'))
    counter += 1
    if counter == 3: break # Limite para testes. Fica mais rapido e não consome toda a cota da API
  return allRoutes

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
  # TODO: depois que o script estiver pronto, remover o limite de 3 neighbors e fazer um loop em todos os servidores usando getRouteServerList()
  serverId = 'BEL-rs1-v4'
  announcedRoutes = getAllAnnouncedRoutesOfServer(serverId)

  neighborComunityDict = {}
  for route in announcedRoutes:
    communitiesList = list(route.get('bgp').get('communities'))
    # TODO: devemos usar só communities ou large communities tambem?
    # largeCommunitiesList = list(neighbor.get('bgp').get('large_communities'))

    # TODO: devemos usar o ID da rota ou o ID do neighbor?
    allRouteCommunities = getAllActionBGPCommunitties(communitiesList)
    if allRouteCommunities:
      neighborComunityDict[route.get('id')] = allRouteCommunities

  displayInformation(neighborComunityDict)