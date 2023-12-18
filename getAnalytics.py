import json

def getTop5MostUsedBGPCommunities():
  mostUsedBGPCommunities = {}
  with open('infos.json', 'r') as infosFile:
     routesAndBGPCommunities = json.load(infosFile).get("infos").get('routesAndBGPCommunities')
     for server in routesAndBGPCommunities:
        mostUsedBGPCommunitiesPerServer = {}
        for route in routesAndBGPCommunities[server]:
          communitiesList = routesAndBGPCommunities[server][route]
          for actionDest in communitiesList:
            action = actionDest[0]
            if action == '65535': # O que fazer com gracefull shutdown?
              continue
            mostUsedBGPCommunitiesPerServer.update({action: mostUsedBGPCommunitiesPerServer.get(action, 0) + 1})
        top5Sorted = sorted(mostUsedBGPCommunitiesPerServer.items(), key=lambda x: x[1], reverse=True)[:5]
        mostUsedBGPCommunities.update({server: top5Sorted})
  return mostUsedBGPCommunities

def getTop1TargetOfBGPCommunities():
  mostUsedBGPCommunities = {}
  with open('infos.json', 'r') as infosFile:
     routesAndBGPCommunities = json.load(infosFile).get("infos").get('routesAndBGPCommunities')
     for server in routesAndBGPCommunities:
        mostUsedBGPCommunitiesPerServer = {}
        for route in routesAndBGPCommunities[server]:
          communitiesList = routesAndBGPCommunities[server][route]
          for actionDest in communitiesList:
            action = actionDest[0]
            if action == '65535': # O que fazer com gracefull shutdown?
              continue
            currentListOfTargets = mostUsedBGPCommunitiesPerServer.get(action, [])
            currentListOfTargets.append(actionDest[1])
            mostUsedBGPCommunitiesPerServer.update({action: currentListOfTargets})
        for action in mostUsedBGPCommunitiesPerServer:
          mostUsedBGPCommunitiesPerServer[action] = max(set(mostUsedBGPCommunitiesPerServer[action]), key=mostUsedBGPCommunitiesPerServer[action].count)
        mostUsedBGPCommunities.update({server: mostUsedBGPCommunitiesPerServer})

  return mostUsedBGPCommunities

if __name__ == '__main__':
  with open('analytics.json', 'w') as f:
    infos = {
      "top5BPGCommunnities": getTop5MostUsedBGPCommunities(),
      "top1TargetOfBGPCommunities": getTop1TargetOfBGPCommunities()
    }
    json.dump({"analytics": infos}, f)