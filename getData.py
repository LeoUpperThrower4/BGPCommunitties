import requests
import json
import time



# Retorna a lista de todos os servidores
def getRouterServerList():
  response = requests.get('https://lg.ix.br/api/v1/routeservers')
  if response.status_code == 200:
    with open('routeservers.json', 'w') as f:
      json.dump(json.loads(response.text), f)
  else:
    print('Error: ' + str(response.status_code))

def getRouteServerNeighbors(serverId) -> list:
  response = requests.get('https://lg.ix.br/api/v1/routeservers/'+serverId+'/neighbors')
  if response.status_code == 200:
    with open("neighbors-"+serverId+".json", 'w') as f:
      json.dump({"neighbors": json.loads(response.text).get("neighbors")}, f)
  else:
    print('Error: ' + str(response.status_code))

def getAnnouncedRoutes(serverId, neighborId, page, value=1):
  response = requests.get('https://lg.ix.br/api/v1/routeservers/'+serverId+'/neighbors/'+neighborId+'/routes/received?page='+str(page))
  if response.status_code == 200:
      return json.loads(response.text)
  else:
    print('Error: ' + neighborId)
    time.sleep(value)
    print('Start another time:' + neighborId)
    if value > 2000: return 
    return getAnnouncedRoutes(serverId, neighborId, page, value*2)
    
def getAllAnnouncedRoutesOfNeighbor(serverId, neighborId):
  currentPage = 0
  allAnnouncedRoutes = []
  with open(serverId+"-announced-"+neighborId+".json", 'w') as f:
    while True:
      announcedRoutes = getAnnouncedRoutes(serverId, neighborId, currentPage)
      if not(announcedRoutes.get('imported')): break

      if announcedRoutes.get('pagination').get('total_pages') == currentPage: break
      # se der problema no loop, sai na centesima pagina
      if currentPage == 100 : break
      allAnnouncedRoutes.extend(announcedRoutes.get('imported'))
      currentPage += 1
    json.dump({"announced":allAnnouncedRoutes}, f)

if __name__ == '__main__':
  # Se quiser usar aquivos X, mude os nomes e comente essa linha
  # getRouterServerList()
  with open('routeservers.json', 'r') as f:
    servers = json.load(f).get('routeservers')
  for server in servers:
    # Se quiser usar aquivos X, mude os nomes e comente essa linha
    # getRouteServerNeighbors(server.get('id'))
    with open("neighbors-"+server.get('id')+".json", 'r') as f:
      neighbors = json.load(f).get('neighbors')
    for neighbor in neighbors:
      getAllAnnouncedRoutesOfNeighbor(server.get('id'), neighbor.get('id'))
      time.sleep(1)
    time.sleep(1)
