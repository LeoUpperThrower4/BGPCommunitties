import json

def merge_lists(list1, list2):
    temp_dict = {}
    for item in list1:
        for key, value in item.items():
          if key not in temp_dict:
            temp_dict[key] = value
          else:
            for v in value:
              if v not in temp_dict[key]:
                temp_dict[key].append(v)

    for item in list2:
        for key, value in item.items():
          if key not in temp_dict:
            temp_dict[key] = value
          else:
            for v in value:
              if v not in temp_dict[key]:
                  temp_dict[key].append(v)

    # Convert the dictionary back to a list of dictionaries
    result = [{key:value} for key, value in temp_dict.items()]

    return result

if __name__ == '__main__':
  with open('routeservers.json', 'r') as serversFile:
    servers = json.load(serversFile).get('routeservers')
    for server in servers:
      with open("results-"+server.get('id')+".json", 'r') as resultsFile:
        results = json.load(resultsFile).get('results')
        neighbor_ids = results.get('neighbors_ids')
        announced_routes_per_neighbor = results.get('announced_routes_per_neighbor')
        announced_bgp_per_router_per_neighbor = results.get('announced_bgp_per_router_per_neighbor')
        new_announced_bgp_per_router_per_neighbor = {}
        new_announced_routes_per_neighbor ={}
        new_neighbor_ids = []
        for neighbor in neighbor_ids:
          neighbor_prefix = neighbor.split('_')[0]
          if not neighbor_prefix in new_neighbor_ids:
            new_neighbor_ids.append(neighbor_prefix)
        for key, value in announced_routes_per_neighbor.items():
          neighbor_prefix = key.split('_')[0]
          if not neighbor_prefix in new_announced_routes_per_neighbor:
            new_announced_routes_per_neighbor.update({neighbor_prefix: value})
          else :
            if len(new_announced_routes_per_neighbor.get(neighbor_prefix)) == 0:
              new_announced_routes_per_neighbor.update({neighbor_prefix: value})
            if len(value) == 0:
              continue
            unionValues = set(new_announced_routes_per_neighbor.get(neighbor_prefix)) | set(value)
            new_announced_routes_per_neighbor.update({neighbor_prefix: list(unionValues)})
            new_announced_routes_per_neighbor.get(neighbor_prefix).extend(value)
        for key, value in announced_bgp_per_router_per_neighbor.items():
          neighbor_prefix = key.split('_')[0]     
          if not neighbor_prefix in new_announced_bgp_per_router_per_neighbor:
            new_announced_bgp_per_router_per_neighbor.update({neighbor_prefix: value})
          else:
            if len(new_announced_bgp_per_router_per_neighbor.get(neighbor_prefix)) == 0:
              new_announced_bgp_per_router_per_neighbor.update({neighbor_prefix: value}) 
            if len(value) == 0:
              continue
            unionList = merge_lists(new_announced_bgp_per_router_per_neighbor.get(neighbor_prefix), value)
            new_announced_bgp_per_router_per_neighbor.update({neighbor_prefix: unionList})

      with open("treatedResults-"+server.get('id')+".json", 'w') as f:
              results = {
                "server_id": server.get('id'),
                "neighbors_ids": new_neighbor_ids,
                "announced_routes_per_neighbor": new_announced_routes_per_neighbor ,
                "announced_bgp_per_router_per_neighbor": new_announced_bgp_per_router_per_neighbor
              }
              json.dump({"results": results}, f)



