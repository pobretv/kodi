#!/usr/bin/python
# coding=utf-8

import sys,xbmcplugin

from resources.lib import pobretv, controlo

try:
	import urlparse
except:
	import urllib.parse

if sys.version[0] == '2':
	params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
else:
	params = dict(urllib.parse.parse_qs(sys.argv[2].replace('?','')))

try: modo = params.get('modo')[0]
except: modo = params.get('modo')
try: url = params.get('url')[0]
except: url = params.get('url')
try: iconimage = params.get('iconimage')[0]
except: iconimage = params.get('iconimage')
try: nome = params.get('nome')[0]
except: nome = params.get('nome')


if modo == None or modo == 'inicio':
	pobretv.pobretv().menu()
elif modo == 'menuFilmes':
	pobretv.pobretv().menuFilmes()
elif modo == 'menuSeries':
	pobretv.pobretv().menuSeries()
elif modo == 'menuAnimes':
	pobretv.pobretv().menuAnimes()
elif modo == 'menuKids':
	pobretv.pobretv().menuKids()
elif modo == 'filmes':
	pobretv.pobretv().filmes(url)
elif modo == 'series':
	pobretv.pobretv().series(url)
elif modo == 'animes':
	pobretv.pobretv().series(url)
elif modo == 'temporadas':
	pobretv.pobretv().temporadas(url)
elif modo == 'episodios':
	pobretv.pobretv().episodios(url)
elif modo == 'pesquisa':
	pobretv.pobretv().pesquisa(url)
elif modo == 'listagemAnos':
	pobretv.pobretv().listagemAnos(url)
elif modo == 'anos':
	pobretv.pobretv().anos(url)
elif modo == 'listagemIdiomas':
	pobretv.pobretv().listagemIdiomas(url)
elif modo == 'idiomas':
	pobretv.pobretv().idiomas(url)
elif modo == 'listagemGeneros':
	pobretv.pobretv().listagemGeneros(url)
elif modo == 'categorias':
	pobretv.pobretv().categorias(url)
elif modo == 'conta':
	pobretv.pobretv().conta()
elif modo == 'favoritos':
	pobretv.pobretv().favoritos(url)
elif modo == 'favoritosMenu':
	pobretv.pobretv().favoritosMenu()
elif modo == 'verdepois':
	pobretv.pobretv().verdepois(url)
elif modo == 'verdepoisMenu':
	pobretv.pobretv().verdepoisMenu()
elif modo == 'aseguir':
	pobretv.pobretv().aseguir(url)
elif modo == 'aseguirMenu':
	pobretv.pobretv().aseguirMenu()
elif modo == 'adicionar-favoritos':
	pobretv.pobretv().adicionarFavoritos(url)
elif modo == 'remover-favoritos':
	pobretv.pobretv().removerFavoritos(url)
elif modo == 'adicionar-agendar':
	pobretv.pobretv().adicionarAgendar(url)
elif modo == 'remover-agendar':
	pobretv.pobretv().removerAgendar(url)
elif modo == 'adicionar-aseguir':
	pobretv.pobretv().adicionarAseguir(url)
elif modo == 'remover-aseguir':
	pobretv.pobretv().removerAseguir(url)
elif modo == 'notificacoes':
	pobretv.pobretv().notificacoes(url)
elif modo == 'mensagens':
	pobretv.pobretv().mensagens(url)
elif modo == 'definicoes':
	pobretv.pobretv().definicoes()
elif modo == 'player':
	pobretv.pobretv().player(url)
elif modo == 'chooseStreamType':
	pobretv.pobretv().chooseStreamType(url)
elif modo == 'marcar-visto':
	pobretv.pobretv().marcarVisto(url)
elif modo == 'marcar-n-visto':
	pobretv.pobretv().marcarNaoVisto(url)
elif modo == 'download':
	pobretv.pobretv().download(url)
elif modo == 'menuTrakt':
	pobretv.pobretv().menuTrakt()
elif modo == 'traktWatchlistFilmes':
	pobretv.pobretv().watchlistFilmes()
elif modo == 'traktWatchlistSeries':
	pobretv.pobretv().watchlistSeries()
elif modo == 'progressoTrakt':
	pobretv.pobretv().progressoTrakt()
elif modo == 'loginTrakt':
	pobretv.pobretv().loginTrakt()
elif modo == 'traktListas':
	pobretv.pobretv().traktListas()
elif modo == 'traktListasItems':
	pobretv.pobretv().traktListasItems(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))