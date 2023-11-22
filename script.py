
import json
# Lista de Comunidades de Ação BGP
# Link: https://docs.ix.br/doc/communities-table-ix-br-v2_0-24112022.pdf
actionBGPCommunitiesList = [
  65000,
  65001,
  64601,
  64602,
  64603,
  65535,
  65002,
  65003,
  65004,
  65010,
  64611,
  64612,
  64613,
  65011,
  64621,
  64622,
  64623
]

def getAllActionBGPCommunitties(communitiesList) -> list:
  participatingCommunities = []
  for community in communitiesList:
    if ((community[0] in actionBGPCommunitiesList) and not(community[0] in participatingCommunities)): 
      participatingCommunities.append(community[0])
  return participatingCommunities


if __name__ == '__main__':
  with open('routeservers.json', 'r') as serversFile:
    servers = json.load(serversFile).get('routeservers')
    for server in servers:
      with open("neighbors-"+server.get('id')+".json", 'r') as neighborsFile:
        neighbors = json.load(neighborsFile).get('neighbors')
        neighbor_ids = []
        announced_routes_per_neighbor = {}
        announced_bgp_per_router_per_neighbor = {}
        for neighbor in neighbors:
          neighbor_ids.append(neighbor.get('id'))
          with open("announced-"+neighbor.get('id')+".json", 'r') as announcedFile:
            announcedRoutes = json.load(announcedFile).get('announced')
            announced_routes_ids = []
            announced_bgp_per_route = []
            for route in announcedRoutes:
              announced_routes_ids.append(route.get('id'))
              communitiesList = list(route.get('bgp').get('communities'))
              allRouteCommunities = getAllActionBGPCommunitties(communitiesList)
              if len(allRouteCommunities) > 0:
                announced_bgp_per_route.append({route.get('id') : allRouteCommunities})
            announced_bgp_per_router_per_neighbor.update({neighbor.get('id') : announced_bgp_per_route})
            announced_routes_per_neighbor.update({neighbor.get('id'): announced_routes_ids})

      with open("results-"+server.get('id')+".json", 'w') as f:
              results = {
                "server_id": server.get('id'),
                "neighbors_ids": neighbor_ids,
                "announced_routes_per_neighbor": announced_routes_per_neighbor ,
                "announced_bgp_per_router_per_neighbor": announced_bgp_per_router_per_neighbor
              }
              json.dump({"results": results}, f)


