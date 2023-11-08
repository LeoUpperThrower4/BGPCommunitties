# Anotações Leo
https://docs.ix.br/doc/communities-table-ix-br-v2_0-24112022.pdf

//Pegar os routeserver
https://lg.ix.br/api/v1/routeservers

//Pegar os neighbors
https://lg.ix.br/api/v1/routeservers/RS-rs1-v4/neighbors

Com o ID dos neighbors a gente consegue ver as rotas anunciadas, usando a seguinte API
https://lg.ix.br/api/v1/routeservers/RS-rs1-v4/neighbors/ID_DONEIGHBOR/routes/received


No dia XX tinham YY membros. Desses, nós vimos ZZ usando pelo menos AA comunidades BGP de ação

"Pra cada localidade, quantos AS utilizam pelo menos uma comunidade de ação (IPV4 e IPV6)"

"O membro ta anunciando 20 rotas e ele usa comunidades de ação. Com que frequeência ele usa? São todas as rotas? Quantos % usam?"
"Quais as comunidades mais populares?"

"O comportamento de uma rede em IPV4 é a mesma em uma IPV6? Analisar as características gerais"



# Semana 2
- ver as mais usadas
- oq um AS faz em SP X tbm faz em RJ?
  - comparar v4 e v6
  - ele nao usa comunidades/nao anuncia

# Anotações Rafael

https://docs.ix.br/doc/communities-table-ix-br-v2_0-24112022.pdf
Lista de route servers: 
https://lg.ix.br/api/v1/routeservers
COmeçar com um, depois extender

Entender quem está conectado:
https://lg.ix.br/api/v1/routeservers/RS-rs1-v4/neighbors

pega os IDS dos vizinhos, ai precisamos ver as rotas anunciadas por eles.
neighboards

Foca as recebidas : received
https://lg.ix.br/api/v1/routeservers/RS-rs1-v4/neighbors/as1031_177_52_38_190/routes/received

após isso recebemos todos os dados, campo imported, cuidado com o page, tem mais de uma página.

https://pedrobmarcos.github.io/papers/comm_conext22.pdf


no dia tal, tinha tantos membros no rio grande do sul,

para cada localidade, no IXBR, quantos ASs utilizam pelo menos alguma comunidade de ação, tanto ipv4, quanto ipv6

x anuncia tantas rotas, e ele usa comunidades de ação, com que frequencia que ele usa, qual percentual, 
quais as comunidades mais populares.

a análise deve ser feita tanto para IPV4 e para IPV6, 

Analisar o comportamente das redes em IPV4 e em IPV6.

Classificação geral, depois analise comportamental de localidades distintas. os vizinhios, ...
