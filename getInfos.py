import json

# Membros totais (IPv4, IPv6) 
def getAllMembers (): 
  membersPerIX = {}
  with open('routeservers.json', 'r') as serversFile:
     servers = json.load(serversFile).get('routeservers')
     for server in servers:
      with open("treatedResults-"+server.get('id')+".json", 'r') as resultsFile:
        results = json.load(resultsFile).get('results')
        numberOfMembers = len(results.get('neighbors_ids'))
        membersPerIX.update({server.get('id'): numberOfMembers})
  return membersPerIX

# Prefixos/Rotas totais (IPv4, IPv6)
def getAllRoutes():
  routesPerIX = {}
  with open('routeservers.json', 'r') as serversFile:
     servers = json.load(serversFile).get('routeservers')
     for server in servers:
      with open("treatedResults-"+server.get('id')+".json", 'r') as resultsFile:
        results = json.load(resultsFile).get('results')
        numberOfRoutes = 0
        for key, value in results.get('announced_routes_per_neighbor').items():
          numberOfRoutes += len(value)
        routesPerIX.update({server.get('id'): numberOfRoutes})
  return routesPerIX

# Membros que anunciam rotas IPv4 e IPv6 com comunidades de ação BGP
def getAllMembersAnnouncingRoutesWithActionBGPCommunities():
  memberAnnouncingBGPPerIX = {}
  with open('routeservers.json', 'r') as serversFile:
     servers = json.load(serversFile).get('routeservers')
     for server in servers:
      with open("treatedResults-"+server.get('id')+".json", 'r') as resultsFile:
        results = json.load(resultsFile).get('results')
        memberAnnoungingBGP = 0
        for key, value in results.get('announced_bgp_per_router_per_neighbor').items():
          if len(value) > 0:
            memberAnnoungingBGP += 1
        memberAnnouncingBGPPerIX.update({server.get('id'): memberAnnoungingBGP})
  return memberAnnouncingBGPPerIX

# Membros que anunciam rotas IPv4 e IPv6 com comunidades de ação BGP 
def getAllRoutesAnnouncedWithActionBGPCommunities():
  routesPerIX = {}
  with open('routeservers.json', 'r') as serversFile:
     servers = json.load(serversFile).get('routeservers')
     for server in servers:
      with open("treatedResults-"+server.get('id')+".json", 'r') as resultsFile:
        results = json.load(resultsFile).get('results')
        numberOfRoutes = 0
        for key, value in results.get('announced_bgp_per_router_per_neighbor').items():
          numberOfRoutes += len(value)
        routesPerIX.update({server.get('id'): numberOfRoutes})
  return routesPerIX

if __name__ == '__main__':
  with open('infos.json', 'w') as f:
    infos = {
      "members": getAllMembers(),
      "routes": getAllRoutes(),
      "membersBGPCommunities": getAllMembersAnnouncingRoutesWithActionBGPCommunities(),
      "routesBGPCommunities": getAllRoutesAnnouncedWithActionBGPCommunities()
    }
    json.dump({"infos": infos}, f)

