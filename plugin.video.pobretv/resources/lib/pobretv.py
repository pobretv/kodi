#!/usr/bin/python
# -*- coding: utf-8 -*-


import json,zlib,hashlib,time,re,os,sys,xbmc,xbmcgui,xbmcplugin,xbmcvfs,pprint, base64
import unicodedata
from . import controlo, Player, URLResolverMedia, Downloader, Database, Trakt, definicoes, utils
import ast
if sys.version[0] == '2':
	reload(sys)  
	sys.setdefaultencoding('utf8')
else:
	import importlib
	importlib.reload(sys)

class pobretv:

	def __init__(self):
		self.API = 'http://api-v1.pobre.tv/'
		#str(base64.urlsafe_b64decode('aHR0cHM6Ly9tcmFwaS54eXov'))
		self.API_SITE = 'http://api-v1.pobre.tv/'
		#str(base64.urlsafe_b64decode('aHR0cHM6Ly9tcmFwaS54eXovYXBpbmV3Lw=='))#aHR0cDovL21wYXBpLm1sL2FwaS8=
		self.SITE = 'http://api-v1.pobre.tv/'
		#str(base64.urlsafe_b64decode('aHR0cDovL21ycGlyYWN5LmdxLw=='))
	def definicoes(self):
		controlo.addon.openSettings()
		controlo.addDir('Entrar novamente','URL1', 'inicio', os.path.join(controlo.artFolder, controlo.skin, 'retroceder.png'))
		#vista_menu()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
	def menu(self):
		login = self.login()
		database = Database.criarFicheiros()
		if not xbmcvfs.exists(controlo.controlFile):
			controlo.dialog.ok('Pobre.tv', 'Devido a atualização interna do Kodi, poderão aparecer erros e estes deverão ser reportados por email.')
			controlo.escrever_ficheiro(controlo.controlFile, '')
			controlo.setSetting(id='utilizadorTrakt', value='')

		if login:
			#evento = self.getEventos()
			#if evento:
				#controlo.addDir('[B]'+evento+'[/B]', self.API_SITE+'evento/1', 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
				#controlo.addDir('', '', '', os.path.join(controlo.artFolder, controlo.skin, 'nada.png'))
			controlo.addDir('Filmes', self.API_SITE+'filmes', 'menuFilmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
			controlo.addDir('Séries', self.API_SITE+'series', 'menuSeries', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
			controlo.addDir('Animes', self.API_SITE+'animes', 'menuAnimes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
			controlo.addDir('Pesquisa', self.API_SITE+'pesquisa.php', 'pesquisa', os.path.join(controlo.artFolder, controlo.skin, 'procurar.png'))
			controlo.addDir('Zona Infantil', '', 'menuKids', os.path.join(controlo.artFolder, controlo.skin, 'zoin.png'))
			controlo.addDir('', '', '', os.path.join(controlo.artFolder, controlo.skin, 'nada.png'))
			if Trakt.loggedIn():
				self.getTrakt()
				#+ self.getNumNotificacoes()   ---- controlo.addDir('Trakt', self.API_SITE+'me', 'menuTrakt', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
			controlo.addDir('A Minha Conta ', self.API_SITE+'me', 'conta', os.path.join(controlo.artFolder, controlo.skin, 'conta.png'))
			controlo.addDir('Definições', self.API_SITE, 'definicoes', os.path.join(controlo.artFolder, controlo.skin, 'definicoes.png'))
			
			
		else:
			controlo.addDir('Alterar Definições', 'URL1', 'definicoes', os.path.join(controlo.artFolder, controlo.skin, 'definicoes.png'))
			controlo.addDir('Entrar novamente', 'URL1', 'inicio', os.path.join(controlo.artFolder, controlo.skin, 'retroceder.png'))
		definicoes.vista_menu()
	def loginTrakt(self):
		Trakt.authTrakt()
		#return None
	def getTrakt(self):
		url = Trakt.__TRAKT_API__+'/users/%s/watched/movies' % controlo.addon.getSetting('utilizadorTrakt').replace('.', '-')
		filmes = Trakt.getTraktAsJson(url, toSave=True)
		url = Trakt.__TRAKT_API__+'/users/%s/watched/shows' % controlo.addon.getSetting('utilizadorTrakt').replace('.', '-')
		series = Trakt.getTraktAsJson(url, toSave=True)
		#insertTraktDB(filmes, series, data)
		url = Trakt.__TRAKT_API__+'/sync/watchlist/movies'
		watchlistFilmes = Trakt.getTraktAsJson(url, toSave=True)
		url = Trakt.__TRAKT_API__+'/sync/watchlist/shows'
		watchlistSeries = Trakt.getTraktAsJson(url, toSave=True)
		url = Trakt.__TRAKT_API__+'/users/%s/watched/shows' % controlo.addon.getSetting('utilizadorTrakt').replace('.', '-')
		progresso = Trakt.getTraktAsJson(url, toSave=True)
		Database.insertTraktDB(filmes, series, watchlistFilmes, watchlistSeries, progresso, controlo.dataHoras)
	def menuFilmes(self):
		controlo.addDir('Todos os Filmes', self.API_SITE+'filmes.php?qualidade='+definicoes.getQualidade(), 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		#controlo.addDir('Filmes em Destaque', self.API_SITE+'filmes/destaque', 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		controlo.addDir('Filmes por Ano', self.API_SITE+'filmes.php?action=ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Filmes por Genero', self.API_SITE+'filmes.php?action=categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		controlo.addDir('Filmes Portugueses', self.API_SITE+'filmes.php?action=lingua&locale=PT-PT&kids=2', 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'fipt.png'))
		controlo.addDir('Filmes por Idioma', self.API_SITE+'filmes.php?action=lingua', 'listagemIdiomas', os.path.join(controlo.artFolder, controlo.skin, 'filid.png'))
		#controlo.addDir('Filmes por Ranking IMDB', self.API_SITE+'filmes/imdbRank/qualidade/'+definicoes.getQualidade(), 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		#controlo.addDir('Filmes para Crianças', self.API_SITE+'filmes/pt/qualidade/'+definicoes.getQualidade(), 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'filmes.png'))
		definicoes.vista_menu()
	def menuTrakt(self):
		controlo.addDir('Progresso', self.API_SITE+'filmes', 'progressoTrakt', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		controlo.addDir('Watchlist Filmes', self.API_SITE+'filmes/destaque', 'traktWatchlistFilmes', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		controlo.addDir('Watchlist Series', self.API_SITE+'filmes/ano', 'traktWatchlistSeries', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		controlo.addDir('Listas Pessoais', self.API_SITE+'filmes/ano', 'traktListas', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		definicoes.vista_menu()
	def menuSeries(self):
		controlo.addDir('Todas as Séries', self.API_SITE+'series.php', 'series', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
		#controlo.addDir('Séries em Destaque', self.API_SITE+'series/destaque', 'series', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
		controlo.addDir('Séries por Ano', self.API_SITE+'series.php?action=ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Séries por Genero', self.API_SITE+'series.php?action=categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		controlo.addDir('Séries Portuguesas', self.API_SITE+'series.php?action=lingua&locale=PT-PT&kids=2', 'series', os.path.join(controlo.artFolder, controlo.skin, 'sept.png'))
		controlo.addDir('Séries por Idioma', self.API_SITE+'series.php?action=lingua', 'listagemIdiomas', os.path.join(controlo.artFolder, controlo.skin, 'seid.png'))
		#controlo.addDir('Séries por Ranking IMDB', self.API_SITE+'series/imdbRank', 'series', os.path.join(controlo.artFolder, controlo.skin, 'series.png'))
		definicoes.vista_menu()
	def menuAnimes(self):
		controlo.addDir('Todos os Animes', self.API_SITE+'animes.php', 'animes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
		#controlo.addDir('Animes em Destaque', self.API_SITE+'animes/destaque', 'animes', os.path.join(controlo.artFolder, controlo.skin, 'animes.png'))
		controlo.addDir('Animes por Ano', self.API_SITE+'animes.php?action=ano', 'listagemAnos', os.path.join(controlo.artFolder, controlo.skin, 'ano.png'))
		controlo.addDir('Animes por Genero', self.API_SITE+'animes.php?action=categoria', 'listagemGeneros', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		#controlo.addDir('Animes por Ranking IMDB', self.API_SITE+'animes/imdbRank', 'animes', os.path.join(controlo.artFolder, controlo.skin, 'generos.png'))
		definicoes.vista_menu()
	def menuKids(self):
		controlo.addDir('Filmes Infatis', self.API_SITE+'filmes.php?action=lingua&locale=PT-PT&kids=1', 'filmes', os.path.join(controlo.artFolder, controlo.skin, 'fiinf.png'))
		controlo.addDir('Séries Infatis', self.API_SITE+'series.php?action=lingua&locale=PT-PT&kids=1', 'series', os.path.join(controlo.artFolder, controlo.skin, 'seinf.png'))
		definicoes.vista_menu()
	def conta(self):
		controlo.addDir('Favoritos', self.API_SITE+'favoritos.php', 'favoritosMenu', os.path.join(controlo.artFolder, controlo.skin, 'favoritos.png'))
		controlo.addDir('Agendados', self.API_SITE+'verdepois.php', 'verdepoisMenu', os.path.join(controlo.artFolder, controlo.skin, 'agendados.png'))
		controlo.addDir('A seguir', self.API_SITE+'aseguir.php', 'aseguirMenu', os.path.join(controlo.artFolder, controlo.skin, 'seguir.png'))
		#controlo.addDir('Notificações', self.API_SITE+'index.php?action=notificacoes', 'notificacoes', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))
		#controlo.addDir('Mensagens', self.API_SITE+'index.php?action=mensagens', 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))
		definicoes.vista_menu()
	def favoritosMenu(self):
		controlo.addDir('Filmes Favoritos', self.API_SITE+'favoritos.php?action=filmes&qualidade='+definicoes.getQualidade(), 'favoritos', os.path.join(controlo.artFolder, controlo.skin, 'fifav.png'))
		controlo.addDir('Séries Favoritas', self.API_SITE+'favoritos.php?action=series', 'favoritos', os.path.join(controlo.artFolder, controlo.skin, 'sefav.png'))
		controlo.addDir('Animes Favoritos', self.API_SITE+'favoritos.php?action=animes', 'favoritos', os.path.join(controlo.artFolder, controlo.skin, 'anfav.png'))
		definicoes.vista_menu()
	def verdepoisMenu(self):
		controlo.addDir('Filmes Agendados', self.API_SITE+'verdepois.php?action=filmes&qualidade='+definicoes.getQualidade(), 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'fiagend.png'))
		controlo.addDir('Séries Agendadas', self.API_SITE+'verdepois.php?action=series', 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'seagend.png'))
		controlo.addDir('Animes Agendados', self.API_SITE+'verdepois.php?action=animes', 'verdepois', os.path.join(controlo.artFolder, controlo.skin, 'anagend.png'))
		definicoes.vista_menu()
	def aseguirMenu(self):
		controlo.addDir('Filmes a Seguir', self.API_SITE+'aseguir.php?action=filmes&qualidade='+definicoes.getQualidade(), 'aseguir', os.path.join(controlo.artFolder, controlo.skin, 'fiseg.png'))
		controlo.addDir('Séries a Seguir', self.API_SITE+'aseguir.php?action=series', 'aseguir', os.path.join(controlo.artFolder, controlo.skin, 'seseg.png'))
		controlo.addDir('Animes a Seguir', self.API_SITE+'aseguir.php?action=animes', 'aseguir', os.path.join(controlo.artFolder, controlo.skin, 'aniseg.png'))
		definicoes.vista_menu()

	def login(self):
		
		if controlo.addon.getSetting('email') == '' or controlo.addon.getSetting('password') == '':
			controlo.alerta('Pobre.tv', 'Precisa de definir o seu email e password')
			return False
		else:
			try:
				post = controlo.urlencode({'username': controlo.addon.getSetting('email'), 'password': controlo.addon.getSetting('password') })
				resultado = controlo.abrir_url(self.API_SITE+'login.php', post=post, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
					return False

				"""try:
					resultado = resultado.decode('utf-8')
				except:
					resultado = resultado.encode('utf-8')"""
				
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'definicoes.pobretv'), resultado)
				#controlo.log(resultado)
				resultado = json.loads(resultado)

				
				try:
					if resultado['codigo'] == 204:
						controlo.alerta('Pobre.tv', resultado['mensagem'])
						return False
				except:
					pass
				token = resultado['cookie']
				refresh = resultado['expira']
				vistos = json.dumps(resultado['vistos'])
				ver_depois = json.dumps(resultado['ver_depois'])
				favoritos = json.dumps(resultado['favoritos'])
				a_seguir = json.dumps(resultado['a_seguir'])
				categorias = resultado['categorias']
				username = resultado['username']
				profile_picture = resultado['profile_pic']
				"""try:
					username = resultado['username'].decode('utf-8')
				except:
					username = resultado['username'].encode('utf-8')"""
				
				xbmc.executebuiltin("Notification(Pobre.tv,"+"Sessão iniciada: "+username+""+","+"6000"+","+ profile_picture +")")
				controlo.addon.setSetting('tokenPobretv', token)
				controlo.addon.setSetting('refreshPobretv', refresh)
				controlo.addon.setSetting('loggedin', username)
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'vistos.pobretv'), vistos)
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'ver_depois.pobretv'), ver_depois)
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'favoritos.pobretv'), favoritos)
				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'a_seguir.pobretv'), a_seguir)

				controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'categorias.pobretv'), categorias)
				
				return True
			except:
				controlo.alerta('Pobre.tv', 'Não foi possível abrir a página. Por favor tente novamente')
				return False

	def getEventos(self):
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenPobretv')
		resultado = controlo.abrir_url(self.API_SITE+'eventos', header=controlo.headers)
		resultado = json.loads(resultado)
		try:
			if resultado['codigo'] == 204:
				controlo.alerta('Pobre.tv', resultado['mensagem'])
				return False
		except:
			pass
		return resultado['data']['nome']
	def getNumNotificacoes(self):
		"""controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenPobretv')
		resultado = controlo.abrir_url(self.API_SITE+'me', header=controlo.headers)
		if resultado == 'DNS':
			controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
			return False
		resultado = json.loads(resultado)"""
		devolve = '[B][COLOR red]'
		devolve += str(controlo.addon.getSetting('notificacoes'))+' notificacoes e '+str(controlo.addon.getSetting('mensagens'))+' mensagens'
		devolve += '[/COLOR][/B]'
		return devolve
	
	def getFavoritos(self,id, content_type):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'favoritos.pobretv'))
		try:
			lista = json.loads(lista)
		except: 
			controlo.log('[ERRO] NÃO CONSEGUIMOS DECIFRAR A LISTA')
			return False
		if not lista:
			return False
		if lista == "" or lista == [] or lista == '[]':
			return False
		for x in lista:
			if str(id) == str(x["content"]) and str(x["content_type"]) == str(content_type):
				return True
		return False
	
	def getVerDepois(self,id, content_type):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'ver_depois.pobretv'))
		try:
			lista = json.loads(lista)
		except: 
			controlo.log('[ERRO] NÃO CONSEGUIMOS DECIFRAR A LISTA')
			return False
		if not lista:
			return False
		if lista == "" or lista == [] or lista == '[]':
			return False
		for x in lista:
			if str(id) == str(x["content"]) and str(x["content_type"]) == str(content_type):
				return True
		return False

	def getASeguir(self,id, content_type):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'a_seguir.pobretv'))
		try:
			lista = json.loads(lista)
		except: 
			controlo.log('[ERRO] NÃO CONSEGUIMOS DECIFRAR A LISTA')
			return False
		if not lista:
			return False
		if lista == "" or lista == [] or lista == '[]':
			return False
		for x in lista:
			if str(id) == str(x["content"]) and str(x["content_type"]) == str(content_type):
				return True
		return False
	
	def getVistoEpisodio(self,id):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'vistos.pobretv'))
		try:
			lista = json.loads(lista)
		except: 
			controlo.log('[ERRO] NÃO CONSEGUIMOS DECIFRAR A LISTA')
			return False
		if not lista:
			return False
		if lista == "" or lista == [] or lista == '[]':
			return False
		for x in lista:
			if str(id) == str(x["content"]) and str(x["content_type"]) == str('ep'):
				return True
		return False
	
	def getVistoFilme(self,id):
		lista = controlo.ler_ficheiro(os.path.join(controlo.pastaDados,'vistos.pobretv'))
		try:
			lista = json.loads(lista)
		except: 
			controlo.log('[ERRO] NÃO CONSEGUIMOS DECIFRAR A LISTA')
			return False
		if not lista:
			return False
		if lista == "" or lista == [] or lista == '[]':
			return False
		for x in lista:
			if str(id) == str(x["content"]) and str(x["content_type"]) == str('m'):
				return True
		return False

	def favoritos(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		controlo.log(resultado)
		if 'filmes' in url:
			tipo = 'filmes'
		elif 'series' in url:
			tipo = 'series'
		elif 'animes' in url:
			tipo = 'animes'
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if tipo == 'filmes':
			for i in resultado['data']:
				self.setFilme(i, vistos, opcao)
		elif tipo == 'series' or tipo == 'animes':
			for i in resultado['data']:
				self.setSeries(i, vistos, opcao, tipo)
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'favoritos')
		definicoes.vista_filmesSeries()
	def verdepois(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if 'filmes' in url:
			tipo = 'filmes'
		elif 'series' in url:
			tipo = 'series'
		elif 'animes' in url:
			tipo = 'animes'
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if tipo == 'filmes':
			for i in resultado['data']:
				self.setFilme(i, vistos, opcao)
				
		elif tipo == 'series' or tipo == 'animes':
			for i in resultado['data']:
				self.setSeries(i, vistos, opcao, tipo)
		
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'verdepois')
		definicoes.vista_filmesSeries()

	def aseguir(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if 'filmes' in url:
			tipo = 'filmes'
		elif 'series' in url:
			tipo = 'series'
		elif 'animes' in url:
			tipo = 'animes'
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if tipo == 'filmes':
			for i in resultado['data']:
				self.setFilme(i, vistos, opcao)
				
		elif tipo == 'series' or tipo == 'animes':
			for i in resultado['data']:
				self.setSeries(i, vistos, opcao, tipo)
		
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'aseguir')
		definicoes.vista_filmesSeries()

	def notificacoes(self, url):
		resultadoa = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		#controlo.log(resultadoa)
		resultadoa = json.loads(resultadoa)
		vistosF = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		for i in resultadoa["data"]:
			if i['tipoVideo'] == 'filme':
				resultado = controlo.abrir_url(self.API_SITE+'filme/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				self.setFilme(i, vistos, opcao)
			elif i['tipoVideo'] == ('serie' or 'anime'):
				resultado = controlo.abrir_url(self.API_SITE+i['tipoVideo']+'/'+str(i['id_video']), header=controlo.headers)
				resultado = json.loads(resultado)
				tipo = tipo+'s'
				self.setSeries(i, vistos, opcao, tipo)

		"""current = resultadoa['meta']['pagination']['current_page']
		total = resultadoa['meta']['pagination']['total_pages']
		try: proximo = resultadoa['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'notificacoes', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))"""
		definicoes.vista_menu()

	def mensagens(self, url):
		resultadoa = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		#controlo.log(resultadoa)
		resultadoa = json.loads(resultadoa)
		for i in resultadoa["data"]:
			controlo.addDir(i['mensagem'], url, 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'notificacoes.png'))

		"""current = resultadoa['meta']['pagination']['current_page']
		total = resultadoa['meta']['pagination']['total_pages']
		try: proximo = resultadoa['meta']['pagination']['links']['next']
		except: pass 
		if current < total:
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, 'mensagens', os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))"""
		definicoes.vista_menu()
	def filmes(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		for i in resultado['data']:
			self.setFilme(i, vistos, opcao)			
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'filmes')
		definicoes.vista_filmesSeries()
	def series(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		for i in resultado['data']:
			self.setSeries(i, vistos, opcao, tipo)
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'series')
		definicoes.vista_filmesSeries()
	def temporadas(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)['data'][0]
		id = url.split('=')[-1]
		
		if 'serie' in url:
			url = self.API_SITE+'series.php?action=temporada&idSerie='+id+'&n=%s'
		elif 'anime' in url:
			url = self.API_SITE+'animes.php?action=temporada&idSerie='+id+'&n=%s'
		try:
			resultado['temporadas'] = resultado['temporadas'].replace('especial', '999')
		except:
			pass
		if resultado['temporadas'] == "":
			return False
		if sys.version[0] == '2':
			for c, i in sorted(json.loads(resultado['temporadas']).iteritems(), key=lambda i: int(i[0])):
				if c != '999':
					controlo.addDir("[B]Temporada[/B] "+str(c), (url % str(c)), 'episodios', os.path.join(controlo.artFolder, controlo.skin,'temporadas', 'temporada'+str(c)+'.png'),poster=self.API+resultado['background'])
				else:
					controlo.addDir("[B]Temporada Especial[/B]", (url % '999'), 'episodios', os.path.join(controlo.artFolder, controlo.skin,'temporadas', 'temporadaEspecial.png'),poster=self.API+resultado['background'])
		else:
			for c, i in sorted(json.loads(resultado['temporadas']).items(), key=lambda i: int(i[0])):
				if c != '999':
					controlo.addDir("[B]Temporada[/B] "+str(c), (url % str(c)), 'episodios', os.path.join(controlo.artFolder, controlo.skin,'temporadas', 'temporada'+str(c)+'.png'),poster=self.API+resultado['background'])
				else:
					controlo.addDir("[B]Temporada Especial[/B]", (url % '999'), 'episodios', os.path.join(controlo.artFolder, controlo.skin,'temporadas', 'temporadaEspecial.png'),poster=self.API+resultado['background'])

		definicoes.vista_temporadas()
	def episodios(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		
		"""controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenPobretv')
		resultadoS = controlo.abrir_url(self.API_SITE+tipo+'/'+url.split('/')[5], header=controlo.headers)
		resultadoS = json.loads(resultadoS)"""
		vistos = Database.selectSeries()
		opcao = controlo.addon.getSetting('marcarVisto')
		naoVisto = False
		numeroParaVer = 0
		temporadaParaVer = 0
		serieParaVer = 0
		episodioParaVer = 0
		contagem = 0
		for i in resultado['data']:
		
			pt = ''
			infoLabels = {'Title': i['nome_episodio'], 'Code': i['imdb'], 'Episode': i['episodio'], 'Season': i['temporada'] }
			try:
				nome = i['nome_episodio'].decode('utf-8')
			except:
				nome = i['nome_episodio'].encode('utf-8')
			br = ''
			final = ''
			semLegenda = ''

			if i['fimtemporada'] == "1":
				final = '[B]Final da Temporada [/B]'
			if i['semlegenda'] == "1":
				semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
			if 'PT' in i['imdb'].upper():
				i['imdb'] = re.compile('(.+?)PT').findall(i['imdb'].upper())[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			imdbSerie = i['fotoSerie'].split('/')[-1].split('.')[0]
			vistoe = False
			cor = 'white'
			visto = False
			vistoa = False
			if opcao == '1' or opcao == '2':
				if self.getVistoEpisodio(i['id_episodio']) == 1:
					vistoa = True
			elif opcao == '0' or opcao == '2':
				vistoa = self.verificarVistoLocal(i['id_serie'], temporada=i['temporada'], episodio=i['episodio'])
			
			if Trakt.loggedIn():			
				ep = i['episodio']
				if '/' in i['episodio']:
					ep = i['episodio'].split('/')[0]
				if 'e' in i['episodio']:
					ep = i['episodio'].split('e')[0]
				for v in json.loads(vistos):
					if v["show"]["ids"]["imdb"] is None:
						visto = False
						continue
					if v["show"]["ids"]["imdb"].upper() != imdbSerie.upper() or v["show"]["ids"]["imdb"]+'PT'.upper() != imdbSerie+'PT'.upper():
						visto = False
						continue
					else:
						for s in v["seasons"]:
							if int(s['number']) == int(i['temporada']):
								for e in s['episodes']:
									if int(e["number"]) == int(ep):
										vistoe = True
										break
									else:
										vistoe = False
			
			if vistoa:
				visto = True
			else:
				visto = False
						
			if vistoe:
				visto = True
				cor = 'blue'
			if visto == False and vistoe == False:
				if naoVisto == False:
					numeroParaVer = i['episodio']
					temporadaParaVer = i['temporada']
					serieParaVer = i['id_serie']
					episodioParaVer = i['id_episodio']
					serieAVer = i['id_serie']
					naoVisto = True
			else:
				contagem = contagem + 1

			if len(i["imagem"]) >= 10:
				imagem = i["imagem"]
			else:
				imagem = i["fotoSerie"]
			try:
				nome = nome.decode('utf-8')
			except:
				nome = str(nome)
    
			if nome == 'Episódio ' +str(i['episodio']):
				nome = ''
			fullname = pt+br+final+semLegenda+'[COLOR '+cor+'][B]Episódio '+str(i['episodio'])+'[/B][/COLOR] '+nome
			controlo.log(str(i['id_episodio']))
			controlo.addVideo(fullname, self.API_SITE+tipo+'.php?action=episodio&idSerie='+str(i['id_serie'])+'&idEpisodio='+str(i['id_episodio']), 'chooseStreamType', imagem, visto, 'episodio', i['temporada'], i['episodio'], infoLabels, i['background'])
		current = resultado['meta']['current']
		total = resultado['meta']['total']
		try: proximo = resultado['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'episodios')
		definicoes.vista_episodios()
		if naoVisto == True:
			if controlo.addon.getSetting('nao-visto-episodios') == 'true':
				if contagem > 0:
					pergunta = controlo.simNao('Pobre.tv', 'Carregar o Episódio #'+str(numeroParaVer)+' da temporada #'+str(temporadaParaVer)+'?')
					if pergunta:
						self.player(self.API_SITE+tipo+'.php?action=episodio&idSerie='+str(serieAVer)+'&idEpisodio='+str(episodioParaVer))
		
	def listagemAnos(self, url):
		anos = [
      		'2022',
			'2021',
			'2020',
			'2019',
			'2018',
			'2017',
			'2016',
			'2015',
			'2014',
			'2013',
			'2012',
			'2011',
			'2010',
			'2009',
			'2008',
			'2007',
			'2006',
			'2000-2005',
			'1990-1999',
			'1980-1989',
			'1970-1979',
			'1960-1969',
			'1950-1959',
			'1900-1949'
		]
		if 'filmes' in url:
			tipo = 0
			qualidade = '&qualidade='+definicoes.getQualidade()
		elif 'series' in url:
			tipo = 1
			qualidade = ''
		elif 'animes' in url:
			tipo = 2
			qualidade = ''
		for i in anos:
			controlo.addDir(i, url+'&ano='+i+qualidade, 'anos', os.path.join(controlo.artFolder, controlo.skin, 'ano', i+'.png'))
		definicoes.vista_menu()
	def listagemIdiomas(self, url):
		idiomas = definicoes.getIdiomas()

		if 'filmes' in url:
			tipo = 0
			qualidade = '&qualidade='+definicoes.getQualidade()
		elif 'series' in url:
			tipo = 1
			qualidade = ''
		elif 'animes' in url:
			tipo = 2
			qualidade = ''
		

		for i in ast.literal_eval(idiomas):
			
			try:
				idioma = i['label'].decode('utf-8')
			except:
				idioma = i['label'].encode('utf-8')
			controlo.addDir(idioma, url+'&locale='+i['id']+qualidade, 'idiomas', os.path.join(controlo.artFolder, controlo.skin, 'bandeiras',  i['id']+'.png'))
		definicoes.vista_menu()

	def listagemGeneros(self, url):
		lista = definicoes.getListCategoria()
		if 'filmes' in url:
			tipo = 0
			qualidade = '&qualidade='+definicoes.getQualidade()
		elif 'series' in url:
			tipo = 1
			qualidade = ''
		elif 'animes' in url:
			tipo = 2
			qualidade = ''
		
		for c in ast.literal_eval(lista):
			if c['movie'] == "1" and (tipo == 1 or tipo == 2):
				continue

			if c['movie'] == "0" and tipo == 0:
				continue
			try:
				cat = c['categorias'].decode('utf-8')
			except:
				cat = c['categorias'].encode('utf-8')
			controlo.addDir(cat, url+'&categoria='+str(c['id_categoria'])+qualidade, 'categorias', os.path.join(controlo.artFolder, controlo.skin, 'genero', c['id_categoria']+'.png'))
		definicoes.vista_menu()

	def idiomas(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultadoa = json.loads(resultado)
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		for i in resultadoa["data"]:
			if 'filme' in url:
				self.setFilme(i, vistos, opcao)
			elif 'serie' in url or 'anime' in url:
				self.setSeries(i, vistos, opcao, tipo)
		current = resultadoa['meta']['current']
		total = resultadoa['meta']['total']
		try: proximo = resultadoa['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'anos')
		definicoes.vista_filmesSeries()

	def anos(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultadoa = json.loads(resultado)
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		for i in resultadoa["data"]:
			if 'filme' in url:
				self.setFilme(i, vistos, opcao)
			elif 'serie' in url or 'anime' in url:
				self.setSeries(i, vistos, opcao, tipo)
		current = resultadoa['meta']['current']
		total = resultadoa['meta']['total']
		try: proximo = resultadoa['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'anos')
		definicoes.vista_filmesSeries()
		
	def categorias(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultadoa = json.loads(resultado)
		vistos = Database.selectFilmes()
		opcao = controlo.addon.getSetting('marcarVisto')
		if 'serie' in url:
			tipo = 'series'
		elif 'anime' in url:
			tipo = 'animes'
		for i in resultadoa["data"]:
			if 'filme' in url:
				self.setFilme(i, vistos, opcao)
			elif 'serie' in url or 'anime' in url:
				self.setSeries(i, vistos, opcao, tipo)
		current = resultadoa['meta']['current']
		total = resultadoa['meta']['total']
		try: proximo = resultadoa['meta']['paginacao']['next']
		except: pass 
		if int(current) < int(total): self.setPagination(current, total, proximo, 'categorias')

		definicoes.vista_filmesSeries()
	def chooseStreamType(self, url):
		options = []
		options.append('Começar a ver')
		options.append('Começar download')
		option = controlo.select('Escolha o tipo de emissão', options)
		controlo.log(option)
		if option == 0:
			self.player(url)
		elif option == 1:
			self.download(url)

	def player(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)[0]
		infolabels = dict()
		
		if 'filme' in url:
			tipo = 'filme'
			infolabels['Code'] = resultado['imdb']
			infolabels['Year'] = resultado['release_year']
			idVideo = resultado['id']
			nome = resultado['original_name']
			temporada = 0
			episodio = 0
			coiso = 'filme'
			_imdb = resultado['imdb']
		else:
			if 'serie' in url:
				tipo = 'serie'
			else:
				tipo = 'anime'
			idVideo = resultado['id_episodio']
			nome = resultado['nome_episodio']
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			_imdb = resultado['imdbSerie']
			coiso = 'outro'

		progressDialog = controlo.progressDialog
		progressDialog.create('Pobre.tv', 'Abrir emissão!\nPor favor aguarde...')
		progressDialog.update(25, 'A obter video e legenda')
		stream, legenda, ext_g = self.getStreamLegenda(idVideo, tipo, coiso=coiso)
		if stream == False and legenda == 204:
			controlo.mensagemprogresso.close()
			controlo.alerta('Pobre.tv', 'Tem de esperar 8 horas até conseguir visualizar algum video.')
			return False
		xbmc.sleep(3000)
		if progressDialog.iscanceled(): return
		progressDialog.update(50, 'Prepara-te, vai começar!')
		xbmc.sleep(1000)
		if progressDialog.iscanceled(): return
		playlist = xbmc.PlayList(1)
		playlist.clear()
		iconimage = ''

		listitem = xbmcgui.ListItem(nome)

		#liz.setInfo( type="Video", infoLabels=infolabels )
		listitem.setInfo(type="Video", infoLabels=infolabels)
		listitem.setArt({ 'icon': 'DefaultVideo.png', 'thumb' : iconimage })
		#listitem.setInfo("Video", {"title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		listitem.setPath(path=stream)
		playlist.add(stream, listitem)

		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

		progressDialog.update(75, 'Boa Sessão!!!')

		if stream == False:
			progressDialog.close()
			controlo.alerta('Pobre.tv', 'O servidor escolhido não disponível, escolha outro ou tente novamente mais tarde.')
		else:

			player_mr = Player.Player(url=url, idFilme=idVideo, pastaData=controlo.pastaDados, temporada=temporada, episodio=episodio, nome=nome, logo=os.path.join(controlo.addonFolder,'icon.png'), imdb=_imdb)

			progressDialog.close()
			player_mr.play(playlist)
			player_mr.setSubtitles(legenda)

			while player_mr.playing:
				xbmc.sleep(5000)
				player_mr.trackerTempo()

	def getStreamLegenda(self, id, tipo, coiso=None):

		if tipo == 'filme':
			url = self.API_SITE+tipo+'s.php?action=links&idFilme='+id
		if tipo == 'serie':
			url = self.API_SITE+tipo+'s.php?action=links&idEpisodio='+id
		if tipo == 'anime':
			url = self.API_SITE+tipo+'s.php?action=links&idEpisodio='+id

		#controlo.log(url)
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		try:
			if resultado['codigo'] == 204:
				controlo.alerta('Pobre.tv', resultado['mensagem'])
				return False, 204, 204
		except: 
			resultado = resultado[0]

		stream = ''
		i = 0
		servidores = []
		titulos = []
		nome = ''
		if resultado['URL1'] != '':
			i+=1
			if 'openload' in resultado['URL1'].lower():
				nome = "OpenLoad"
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'vidzi' in resultado['URL1'].lower():
				nome = 'Vidzi'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'google' in resultado['URL1'].lower() or 'cloud.mail.ru' in resultado['URL1'].lower():
				nome = 'Pobre.tv'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'uptostream' in resultado['URL1'].lower():
				nome = 'UpToStream'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'rapidvideo.com' in resultado['URL1'].lower() or 'raptu' in resultado['URL1'].lower():
				nome = 'Raptu'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'vidoza.net' in resultado['URL1'].lower():
				nome = 'Vidoza'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'streamango.' in resultado['URL1'].lower():
				nome = 'Streamango'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'mixdrop.' in resultado['URL1'].lower():
				nome = 'Mixdrop'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'fembed' in resultado['URL1'].lower():
				nome = 'Fembed'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'mystream' in resultado['URL1'].lower():
				nome = 'MyStream'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'streamtape.' in resultado['URL1'].lower():
				nome = 'Streamtape'
				servidores.append(resultado['URL1'])
				titulos.append('Servidor #%s: %s' % (i, nome))
		if resultado['URL2'] != '':
			i+=1
			if 'openload' in resultado['URL2'].lower():
				nome = "OpenLoad"
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'vidzi' in resultado['URL2'].lower():
				nome = 'Vidzi'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'google' in resultado['URL2'].lower() or 'cloud.mail.ru' in resultado['URL2'].lower():
				nome = 'Pobre.tv'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'uptostream.com' in resultado['URL2'].lower():
				nome = 'UpToStream'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'rapidvideo.com' in resultado['URL2'].lower() or 'raptu' in resultado['URL2'].lower():
				nome = 'Raptu'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'vidoza.net' in resultado['URL2'].lower():
				nome = 'Vidoza'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'streamango.' in resultado['URL2'].lower():
				nome = 'Streamango'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'mixdrop.' in resultado['URL2'].lower():
				nome = 'Mixdrop'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'fembed' in resultado['URL2'].lower():
				nome = 'Fembed'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'mystream' in resultado['URL2'].lower():
				nome = 'MyStream'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
			elif 'streamtape.' in resultado['URL2'].lower():
				nome = 'Streamtape'
				servidores.append(resultado['URL2'])
				titulos.append('Servidor #%s: %s' % (i, nome))
		try:
			if resultado['URL3'] != '':
				i+=1
				if 'openload' in resultado['URL3'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL3'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL3'].lower() or 'cloud.mail.ru' in resultado['URL3'].lower():
					nome = 'Pobre.tv'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL3'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL3'].lower() or 'raptu' in resultado['URL3'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL3'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL3'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.' in resultado['URL3'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'fembed' in resultado['URL3'].lower():
					nome = 'Fembed'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mystream' in resultado['URL3'].lower():
					nome = 'MyStream'
					servidores.append(resultado['URL3'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass
		try:
			if resultado['URL4'] != '':
				i+=1
				if 'openload' in resultado['URL4'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL4'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL4'].lower() or 'cloud.mail.ru' in resultado['URL4'].lower():
					nome = 'Pobre.tv'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL4'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL4'].lower() or 'raptu' in resultado['URL4'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL4'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL4'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.' in resultado['URL4'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'fembed' in resultado['URL4'].lower():
					nome = 'Fembed'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mystream' in resultado['URL4'].lower():
					nome = 'MyStream'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamtape.' in resultado['URL4'].lower():
					nome = 'Streamtape'
					servidores.append(resultado['URL4'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass

		try:
			if resultado['URL5'] != '':
				i+=1
				if 'openload' in resultado['URL5'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL5'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL5'].lower() or 'cloud.mail.ru' in resultado['URL5'].lower():
					nome = 'Pobre.tv'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL5'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL5'].lower() or 'raptu' in resultado['URL5'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL5'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL5'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.' in resultado['URL5'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'fembed' in resultado['URL5'].lower():
					nome = 'Fembed'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mystream' in resultado['URL5'].lower():
					nome = 'MyStream'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamtape.' in resultado['URL5'].lower():
					nome = 'Streamtape'
					servidores.append(resultado['URL5'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass

		try:
			if resultado['URL6'] != '':
				i+=1
				if 'openload' in resultado['URL6'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL6'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL6'].lower() or 'cloud.mail.ru' in resultado['URL6'].lower():
					nome = 'Pobre.tv'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL6'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL6'].lower() or 'raptu' in resultado['URL6'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL6'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL6'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.' in resultado['URL6'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'fembed' in resultado['URL6'].lower():
					nome = 'Fembed'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mystream' in resultado['URL6'].lower():
					nome = 'MyStream'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamtape.' in resultado['URL6'].lower():
					nome = 'Streamtape'
					servidores.append(resultado['URL6'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass

		try:
			if resultado['URL7'] != '':
				i+=1
				if 'openload' in resultado['URL7'].lower():
					nome = "OpenLoad"
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidzi' in resultado['URL7'].lower():
					nome = 'Vidzi'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'google' in resultado['URL7'].lower() or 'cloud.mail.ru' in resultado['URL7'].lower():
					nome = 'Pobre.tv'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'uptostream.com' in resultado['URL7'].lower():
					nome = 'UpToStream'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'rapidvideo.com' in resultado['URL7'].lower() or 'raptu' in resultado['URL7'].lower():
					nome = 'Raptu'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'vidoza.net' in resultado['URL7'].lower():
					nome = 'Vidoza'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamango.' in resultado['URL7'].lower():
					nome = 'Streamango'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mixdrop.' in resultado['URL7'].lower():
					nome = 'Mixdrop'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'fembed' in resultado['URL7'].lower():
					nome = 'Fembed'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'mystream' in resultado['URL7'].lower():
					nome = 'MyStream'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
				elif 'streamtape.' in resultado['URL7'].lower():
					nome = 'Streamtape'
					servidores.append(resultado['URL7'])
					titulos.append('Servidor #%s: %s' % (i, nome))
		except:
			pass

		legenda = ''

		"""for s in servidores:
			#controlo.log(s)
		for l in titulos:
			#controlo.log(l)"""

		legenda = resultado['legenda']
		try:
			if resultado['semlegenda'] == "1":
				legenda = ''
		except:
			pass
		try:
			if resultado['legenda'] == "semlegenda":
				legenda = ''
		except:
			pass
		legendaAux = legenda
		ext_g = 'coiso'
		servidor = 0
		if controlo.addon.getSetting('melhor-fonte') == 'true':
			i = 0
			for nome in titulos:
				if 'Pobre.tv' in nome:
					servidor = i
					break
				if 'OpenLoad' in nome:
					servidor = i
				i = i+1

		else:	
			if len(titulos) > 1:
				servidor = controlo.select('Escolha o servidor', titulos)
			else:
				servidor = 0

		if 'vidzi' in servidores[servidor]:
			vidzi = URLResolverMedia.Vidzi(servidores[servidor])
			stream = vidzi.getMediaUrl()
			legenda = vidzi.getSubtitle()
		elif 'uptostream.com' in servidores[servidor]:
			stream = URLResolverMedia.UpToStream(servidores[servidor]).getMediaUrl()
		elif 'server.pobre.tv' in servidores[servidor]:
			stream = servidores[servidor]
		elif 'openload' in servidores[servidor]:
			stream = URLResolverMedia.OpenLoad(servidores[servidor]).getMediaUrl()
			"""legenda = URLResolverMedia.OpenLoad(servidores[servidor]).getSubtitle()
			if not '.vtt' in legenda or legenda == '':
				legenda = legendaAux"""
		elif 'drive.google.com/' in servidores[servidor]:
			stream, ext_g = URLResolverMedia.GoogleVideo(servidores[servidor]).getMediaUrl()
		elif 'cloud.mail.ru' in servidores[servidor]:
			stream, ext_g = URLResolverMedia.CloudMailRu(servidores[servidor]).getMediaUrl()
		elif 'rapidvideo.com' in servidores[servidor] or 'raptu' in servidores[servidor]:
			rapid = URLResolverMedia.RapidVideo(servidores[servidor])
			stream = rapid.getMediaUrl()
			legenda = rapid.getLegenda()
		elif 'vidoza.net' in servidores[servidor]:
			vidoz = URLResolverMedia.Vidoza(servidores[servidor])
			stream = vidoz.getMediaUrl()
			legenda = vidoz.getLegenda()
		elif 'streamango.' in servidores[servidor]:
			streaman = URLResolverMedia.Streamango(servidores[servidor])
			stream = streaman.getMediaUrl()
			legenda = streaman.getLegenda()
		elif 'mixdrop.' in servidores[servidor]:
			mixdrop = URLResolverMedia.Mixdrop(servidores[servidor])
			stream = mixdrop.getMediaUrl()
			legenda = mixdrop.getLegenda()
		elif 'fembed' in servidores[servidor]:
			fembed = URLResolverMedia.Fembed(servidores[servidor])
			stream = fembed.getMediaUrl()
			legenda = fembed.getLegenda()
		elif 'mystream' in servidores[servidor]:
			mystream = URLResolverMedia.MyStream(servidores[servidor])
			stream = mystream.getMediaUrl()
			legenda = mystream.getLegenda()
		elif 'streamtape.' in servidores[servidor].lower():
			streamtape = URLResolverMedia.Streamtape(servidores[servidor])
			stream = streamtape.getMediaUrl()
			legenda = streamtape.getLegenda()

		"""if coiso == 'filme':
			legenda = legendaAux
			if resultado['imdb'] not in legenda:
				legenda = self.API+'subs/%s.srt' % resultado['imdb']"""

		if legenda == '':
			legenda = legendaAux
		return stream, legenda, ext_g

	def pesquisa(self, url):
		vistos = Database.selectFilmes()
		qualidade = ''
		if 'filmes' in url:
			ficheiro = os.path.join(controlo.pastaDados,'filmes_pesquisa.pobretv')
			tipo = 0
			qualidade = definicoes.getQualidade()
		elif 'series' in url:
			ficheiro = os.path.join(controlo.pastaDados,'series_pesquisa.pobretv')
			tipo = 1
			qualidade = '2'
			site = 'series'
		elif 'animes' in url:
			ficheiro = os.path.join(controlo.pastaDados,'animes_pesquisa.pobretv')
			tipo = 2
			qualidade = '2'
			site = 'animes'

		if 'page' not in url:
			try:
				tipo = controlo.select(u'Onde quer pesquisar?', ['Filmes', 'Series', 'Animes'])
			except:
				return False
			teclado = controlo.teclado('', 'O que quer pesquisar?')
			if tipo == 0:
				url = self.API_SITE+'filmes.php?action=pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'filmes_pesquisa.pobretv')
				qualidade = definicoes.getQualidade()
			elif tipo == 1:
				url = self.API_SITE+'series.php?action=pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'series_pesquisa.pobretv')
				qualidade = '2'
				site = 'series'
			elif tipo == 2:
				url = self.API_SITE+'animes.php?action=pesquisa'
				ficheiro = os.path.join(controlo.pastaDados,'animes_pesquisa.pobretv')
				qualidade = '2'
				site = 'animes'
				
			if xbmcvfs.exists(ficheiro):
				f = open(ficheiro, "r")
				texto = f.read()
				f.close()
				teclado.setDefault(texto)
			teclado.doModal()
			
			if teclado.isConfirmed():
				strPesquisa = teclado.getText()
				dados = controlo.urlencode({'texto': strPesquisa, 'qualidade': qualidade})
				try:
					f = open(ficheiro, mode="w")
					f.write(strPesquisa)
					f.close()
				except:
					traceback.print_exc()
					controlo.log("Não gravou o conteudo em %s" % ficheiro)

				resultado = controlo.abrir_url(url,post=dados, header=controlo.headers, cookie=definicoes.getCookie())
		else:
			if xbmcvfs.exists(ficheiro):
				f = open(ficheiro, "r")
				texto = f.read()
				f.close()
			dados = controlo.urlencode({'texto': texto, 'qualidade':qualidade})
			resultado = controlo.abrir_url(url,post=dados, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)

		try:
			if resultado['codigo'] == 204:
				controlo.alerta('Pobre.tv', 'Deve Indicar um valor para pesquisa.')
			return False
		except:
			resultado = resultado

		opcao = controlo.addon.getSetting('marcarVisto')

		if resultado['data'] != '':
			if tipo == 0:
				for i in resultado['data']:
					self.setFilme(i, vistos, opcao)
			elif tipo == 1 or tipo == 2:
				for i in resultado['data']:
					self.setSeries(i, vistos, opcao, site)

			current = resultado['meta']['current']
			total = resultado['meta']['total']
			try: proximo = resultado['meta']['paginacao']['next']
			except: pass 
			if int(current) < int(total): self.setPagination(current, total, proximo, 'pesquisa')
		definicoes.vista_filmesSeries()
	
	def changeContentWatchStatus(self, url):
     
		contentJson = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		contentJson = json.loads(contentJson)[0]

		if 'filme' in url:
			movieId = contentJson['id']
			contentImdb = contentJson['imdb']
			contentType = 'movie'
			markContentAsWatchedEndpoint = self.API_SITE + 'index.php?action=marcar-visto-filme&idFilme=' + str(movieId)
		else:
			episodeId = contentJson['id_episodio']
			contentImdb = contentJson['imdbSerie']
			contentType = 'tvshow'
			episodeSeason = contentJson['temporada']
			episodeNumber = contentJson['episodio']
			markContentAsWatchedEndpoint = self.API_SITE+'index.php?action=marcar-visto-episodio&idEpisodio=' + str(episodeId)

		contentWatchedEndpointResponse = controlo.abrir_url(markContentAsWatchedEndpoint, header = controlo.headers, cookie = definicoes.getCookie())
		contentWatchedEndpointResponse = json.loads(contentWatchedEndpointResponse)

		if contentWatchedEndpointResponse['mensagem']['codigo'] == 200:
			stateOfUserWatchedInteraction = 1 #Marked as watched
		if contentWatchedEndpointResponse['mensagem']['codigo'] == 201:
			stateOfUserWatchedInteraction = 2 #Unmarked as watched
		elif contentWatchedEndpointResponse['mensagem']['codigo'] == 204:
			stateOfUserWatchedInteraction = 3 # Error
			
		if stateOfUserWatchedInteraction == 3:
			controlo.alerta('Pobre.tv', contentWatchedEndpointResponse['mensagem']['mensagem'])
			return False
			
		allUserWatchInteractionsJson = json.dumps(contentWatchedEndpointResponse['userVistos'])
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados, 'vistos.pobretv'), allUserWatchInteractionsJson)

		if Trakt.loggedIn() and stateOfUserWatchedInteraction == 1:
			if 'PT' in contentImdb:
				contentImdb = re.compile('(.+?)PT').findall(contentImdb)[0]
				
			if 'pt' in contentImdb:
				contentImdb = re.compile('(.+?)pt').findall(contentImdb)[0]
				
			if contentType == 'tvshow':
				Trakt.markwatchedEpisodioTrakt(contentImdb, episodeSeason, episodeNumber)
			else:
				Trakt.markwatchedFilmeTrakt(contentImdb)
    
			self.getTrakt()

		if stateOfUserWatchedInteraction == 1:
			xbmc.executebuiltin("Notification(Pobre.tv," + "Marcado como visto" + "," + "6000" + "," + os.path.join(controlo.addonFolder,'icon.png') + ")")
			xbmc.executebuiltin("Container.Refresh")
		if stateOfUserWatchedInteraction == 2:
			xbmc.executebuiltin("Notification(Pobre.tv," + "Marcado como não visto" + "," + "6000" + "," + os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
		elif stateOfUserWatchedInteraction == 3:
			controlo.alerta('Pobre.tv', 'Ocorreu um erro ao marcar como visto')
		return True
 
	def marcarVisto(self, url):
     
		self.changeContentWatchStatus(url)
  
	def marcarNaoVisto(self, url):
     
		self.changeContentWatchStatus(url)

	def download(self, url):
		resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)[0]
		
		links = url.split('/')
		folder = xbmcvfs.translatePath(controlo.addon.getSetting('pastaDownloads'))
		if len(folder) <= 3:
			controlo.alerta('Pobre.tv', 'Tens de definir uma pasta de download nas definições.')
			return False

		if 'filme' in url:
			tipo = 'filme'
			tipo_desc = 'filme'
			idVideo = resultado['id']
			nome = str(resultado['original_name']) + " (" + str(resultado['release_year']) + ")"
			temporada = 0
			episodio = 0
			coiso = 'filme'
			_imdb = resultado['imdb']
		else:
			if 'serie' in url:
				tipo = 'serie'
			else:
				tipo = 'anime'
			idVideo = resultado['id_episodio']
			nomeSerie = resultado['nomeSerie']
			nome = str(nomeSerie) + " - " + " S" + str(resultado['temporada']) + "E" + str(resultado['episodio']) + " " +  str(resultado['nome_episodio'])
			temporada = resultado['temporada']
			episodio = resultado['episodio']
			_imdb = resultado['imdbSerie']
			coiso = 'outro'
   
   

		progressDialog = controlo.progressDialog
		progressDialog.create('Pobre.tv', 'Abrir emissão!\nPor favor aguarde...')
		progressDialog.update(25, 'Obter video e legenda')
		stream, legenda, ext_g = self.getStreamLegenda(idVideo, tipo, coiso=coiso)
		if stream == False and legenda == 204:
			progressDialog.close()
			controlo.alerta('Pobre.tv', 'Tem de esperar 8 horas até conseguir fazer download de algum video.')
			return False
		xbmc.sleep(3000)
		if progressDialog.iscanceled(): return
		progressDialog.update(50, 'O download vai começar!')
		xbmc.sleep(1000)
		if progressDialog.iscanceled(): return

		legendasOn = False
		
		if legenda != '':
			legendasOn = True
		if tipo != 'filme':
			if not xbmcvfs.exists(os.path.join(folder,'Séries')):
				xbmcvfs.mkdirs(os.path.join(folder,'Séries'))
			if not xbmcvfs.exists(os.path.join(folder,'Séries', self.clean(nomeSerie))):
				xbmcvfs.mkdirs(os.path.join(folder,'Séries', self.clean(nomeSerie)))
			if not xbmcvfs.exists(os.path.join(folder,'Séries',self.clean(nomeSerie), "Temporada " + str(temporada))):
				xbmcvfs.mkdirs(os.path.join(folder,'Séries',self.clean(nomeSerie), "Temporada " + str(temporada)))
			folder = os.path.join(folder, 'Séries', self.clean(nomeSerie), "Temporada " + str(temporada))
			name = self.clean(nome)
		else:
			if not xbmcvfs.exists(os.path.join(folder,'Filmes')):
				xbmcvfs.mkdirs(os.path.join(folder,'Filmes'))
			folder = os.path.join(folder,'Filmes')
			name = self.clean(nome)

		streamAux = self.clean(stream.split('/')[-1])
		extensaoStream = self.clean(streamAux.split('.')[-1])

		if '?mim' in extensaoStream:
			extensaoStream = re.compile('(.+?)\?mime=').findall(extensaoStream)[0]


		if ext_g != 'coiso':
			extensaoStream = ext_g

		extensaoStream = 'mp4'

		nomeStream = name+'.'+extensaoStream	

		Downloader.Downloader().download(os.path.join(folder, nomeStream), stream, nomeStream)
		
		if legendasOn:
			#controlo.log(legenda)
			legendaAux = self.clean(legenda.split('/')[-1])
			extensaoLegenda = self.clean(legendaAux.split('.')[-1])
			#controlo.log(extensaoLegenda)
			nomeLegenda = name+'.'+extensaoLegenda
			self.download_legendas(legenda, os.path.join(folder, nomeLegenda))

	def download_legendas(self,url,path):
		contents = controlo.abrir_url(url, header=controlo.headers)
		if contents:
			fh = open(path, 'wb')
			fh.write(contents)
			fh.close()
		return
	def clean(self, text):
		command={'&#8220;':'"','&#8221;':'"', '&#8211;':'-','&amp;':'&','&#8217;':"'",'&#8216;':"'"}
		regex = re.compile("|".join(map(re.escape, command.keys())))
		return regex.sub(lambda mo: command[mo.group(0)], text)
	def progressoTrakt(self):

		vistos = Database.selectProgresso()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenPobretv')

		for serie in json.loads(vistos):
			url = 'https://api-v2launch.trakt.tv/shows/%s/progress/watched?hidden=false&specials=false' % serie["show"]["ids"]["slug"]
			data = Trakt.getTraktAsJson(url)
			if data == "asd":
				continue
			data = json.loads(data)
		
			try:
				episodioN = str(data["next_episode"]["number"])
				temporadaNumero = str(data["next_episode"]["season"])
			except:
				continue

			if serie["show"]["ids"]["imdb"] is None:
				continue

			
			url = self.API_SITE+'serie/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"],temporadaNumero, episodioN )
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			tipo = 'serie'
			try:
				resultado = json.loads(resultado)
			except ValueError:
				continue
			if 'codigo' in resultado:
				url = self.API_SITE+'serie/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"]+'PT',temporadaNumero, episodioN )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				url = self.API_SITE+'anime/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"],temporadaNumero, episodioN )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				url = self.API_SITE+'anime/%s/temporada/%s/episodio/%s/imdb' % (serie["show"]["ids"]["imdb"]+'PT',temporadaNumero, episodioN )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				continue
			url = self.API_SITE+'serie/%s' % (resultado['id_serie'])
			resultadoS = controlo.abrir_url(url, header=controlo.headers)
			if resultadoS == 'DNS':
				controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			tipo = 'serie'
			try:
				resultadoS = json.loads(resultadoS)
			except ValueError:
				continue
			if 'codigo' in resultadoS:
				url = self.API_SITE+'anime/%s' % (resultado['id_serie'])
				resultadoS = controlo.abrir_url(url, header=controlo.headers)
				if resultadoS == 'DNS':
					controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				
				try:
					resultadoS = json.loads(resultadoS)
				except ValueError:
					continue
		

			if resultado['URL1'] == '' and resultado['URL2'] == '':
				continue

			infoLabels = {'Title': resultado['nome_episodio'], 'Code': resultado['imdb'], 'Episode': resultado['episodio'], 'Season': resultado['temporada'] }
			try:
				nome = resultado['nome_episodio'].decode('utf-8')
			except:
				nome = resultado['nome_episodio'].encode('utf-8')
			imagem = ''
			if resultado['imagem'] == "1":
				imagem = self.API+'images/series/'+resultado['imdb']+'.jpg'
			elif resultado['imagem'] == "0":
				imagem = self.API+'images/capas/'+resultado['imdbSerie']+'.jpg'
			categoria = resultadoS['category1']
			if resultadoS['category2'] != '':
				categoria += ','+resultadoS['category2']
			if resultadoS['category3'] != '':
				categoria += ','+resultadoS['category3']
			pt = ''
			br = ''
			final = ''
			semLegenda = ''
			if resultado['fimtemporada'] == "1":
				final = '[B]Final da Temporada [/B]'
			if resultado['semlegenda'] == "1":
				semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			if 'PT' in resultado['imdb']:
				resultado['imdb'] = re.compile('(.+?)PT').findall(resultado['imdb'].upper())[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			controlo.addVideo(pt+br+semLegenda+final+'[B]'+resultado['nomeSerie']+'[/B] '+temporadaNumero+'x'+episodioN+' . '+nome, self.API_SITE+tipo+'/'+str(resultado['id_serie'])+'/temporada/'+str(resultado['temporada'])+'/episodio/'+str(resultado['episodio']), 'chooseStreamType', imagem, False, 'episodio', resultado['temporada'], resultado['episodio'], infoLabels, self.API+resultado['background'])
		definicoes.vista_filmesSeries()
		xbmc.executebuiltin("Container.SetViewMode(50)")
	def watchlistFilmes(self):
		vistos = Database.selectWatchFilmes()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenPobretv')
		opcao = controlo.addon.getSetting('marcarVisto')
		for f in json.loads(vistos):
			if f["movie"]["ids"]["imdb"] is None:
				continue
			imdb = f["movie"]["ids"]["imdb"]
			url = self.API_SITE+'filme/%s/imdb/qualidade/%s' % (imdb, definicoes.getQualidade())
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			resultado = json.loads(resultado)
			if 'codigo' in resultado:
				continue
			categoria = resultado['category1']
			if resultado['category2'] != '':
				categoria += ','+resultado['category2']
			if resultado['category3'] != '':
				categoria += ','+resultado['category3']
			
			pt = ''
			br = ''
			semLegenda = ''
			if resultado['legenda'] == "semlegenda":
				semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
			if 'Brasileiro' in categoria:
				br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
			if 'Portu' in categoria:
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'

			if 'PT' in resultado['imdb']:
				resultado['imdb'] = re.compile('(.+?)PT').findall(resultado['imdb'].upper())[0]
				pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
			visto = False
			if opcao == '1' or opcao == '2':
				if resultado['visto'] == 1:
					visto = True
			elif opcao == '0' or opcao == '2':
				visto = self.verificarVistoLocal(resultado['id_video'])
			infoLabels = {'Title': resultado['original_name'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['imdb'] }
			
			try:
				nome = resultado['original_name'].decode('utf-8')
			except:
				nome = resultado['original_name'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = self.API+'images/capas/'+resultado['foto'].split('/')[-1]

			if resultado['verdepois'] == 1:
				menuVerDepois = True
			else:
				menuVerDepois = False

			if resultado['favorito'] == 1:
				menuFavorito = True
			else:
				menuFavorito = False
			controlo.addVideo(pt+br+semLegenda+nome+' ('+resultado['ano']+')', self.API_SITE+'filme/'+str(resultado['id_video']), 'chooseStreamType', resultado['foto'],visto, 'filme', 0, 0, infoLabels, self.API+resultado['background'], trailer=resultado['trailer'], favorito=menuFavorito, agendado=menuVerDepois)
		definicoes.vista_filmesSeries()

	def watchlistSeries(self):
		vistos = Database.selectWatchSeries()
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenPobretv')
		for s in json.loads(vistos):
			if s["show"]["ids"]["imdb"] is None:
				continue
			imdb = s["show"]["ids"]["imdb"]
		
			
			url = self.API_SITE+'serie/%s/imdb' % (s["show"]["ids"]["imdb"] )
			resultado = controlo.abrir_url(url, header=controlo.headers)
			if resultado == 'DNS':
				controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
				return False
			tipo = 'serie'
			try:
				resultado = json.loads(resultado)
			except ValueError:
				continue
			if 'codigo' in resultado:
				url = self.API_SITE+'anime/%s/imdb' % (s["show"]["ids"]["imdb"] )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'anime'
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
			if 'codigo' in resultado:
				continue
			

			categoria = resultado['category1']
			if resultado['category2'] != '':
				categoria += ','+resultado['category2']
			if resultado['category3'] != '':
				categoria += ','+resultado['category3']

			infoLabels = {'Title': resultado['original_name'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['imdb'] }
		
			try:
				nome = resultado['original_name'].decode('utf-8')
			except:
				nome = resultado['original_name'].encode('utf-8')
			if 'http' not in resultado['foto']:
				resultado['foto'] = self.API+'images/capas/'+resultado['foto'].split('/')[-1]
			if resultado['visto'] == 1:
				visto=True
			else:
				visto=False
			if resultado['verdepois'] == 1:
				menuVerDepois = True
			else:
				menuVerDepois = False

			if resultado['favorito'] == 1:
				menuFavorito = True
			else:
				menuFavorito = False
			controlo.addDir(nome+' ('+resultado['ano']+')', self.API_SITE+tipo+'/'+str(resultado['id_video']), 'temporadas', resultado['foto'], tipo='serie', infoLabels=infoLabels,poster=self.API+resultado['background'],visto=visto, menuO=True, favorito=menuFavorito, agendado=menuVerDepois)
		definicoes.vista_filmesSeries()
	def remove_accents(self, text):
		return self.clean(text)

	def verificarVistoLocal(self, idVideo, temporada=None, episodio=None):
		pastaVisto=os.path.join(controlo.pastaDados,'vistos')

		if temporada and episodio:
			ficheiroVisto = os.path.join(pastaVisto,str(idVideo)+'_S'+str(temporada)+'x'+str(episodio)+'.pobretv')
		else:
			ficheiroVisto = os.path.join(pastaVisto,str(idVideo)+'.pobretv')

		if os.path.exists(ficheiroVisto):
			return True
		else:
			return False

	def adicionarFavoritos(self, url):
	
		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id']
			tipo = 0
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=adicionar&tipo=filme&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 1
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=adicionar&tipo=serie&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 2
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=adicionar&tipo=anime&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		favoritos = json.dumps(resultado['favoritos'])

		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'favoritos.pobretv'), favoritos)

		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("Notification(Pobre.tv,"+nome+": Adicionado aos Favoritos"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")
	def removerFavoritos(self, url):
		
		links = url.split('/')
		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id']
			tipo = 0
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=remover&tipo=filme&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 1
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=remover&tipo=serie&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers,cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 2
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'favoritos.php?action=remover&tipo=anime&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		favoritos = json.dumps(resultado['favoritos'])
				
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'favoritos.pobretv'), favoritos)
		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("Notification(Pobre.tv,"+nome+": Removido dos Favoritos"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def adicionarAgendar(self, url):

		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id']
			tipo = 0
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=adicionar&tipo=filme&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 1
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=adicionar&tipo=serie&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 2
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=adicionar&tipo=anime&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		ver_depois = json.dumps(resultado['ver_depois'])
				
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'ver_depois.pobretv'), ver_depois)
		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("Notification(Pobre.tv,"+nome+": Agendado"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def removerAgendar(self, url):
		
		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id']
			tipo = 0
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=remover&tipo=filme&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 1
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=remover&tipo=serie&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 2
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'verdepois.php?action=remover&tipo=anime&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		ver_depois = json.dumps(resultado['ver_depois'])
				
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'ver_depois.pobretv'), ver_depois)
		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("Notification(Pobre.tv,"+nome+": Removido dos Agendados"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def adicionarAseguir(self, url):

		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id']
			tipo = 0
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'aseguir.php?action=adicionar&tipo=filme&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 1
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'aseguir.php?action=adicionar&tipo=serie&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 2
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'aseguir.php?action=adicionar&tipo=anime&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		a_seguir = json.dumps(resultado['a_seguir'])
				
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'a_seguir.pobretv'), a_seguir)
		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("Notification(Pobre.tv,"+nome+": A seguir"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def removerAseguir(self, url):
		
		if 'filme' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)[0]
			id_video = resultado['id']
			tipo = 0
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'aseguir.php?action=remover&tipo=filme&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'serie' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 1
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'aseguir.php?action=remover&tipo=serie&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		elif 'anime' in url:
			resultado = controlo.abrir_url(url, header=controlo.headers, cookie=definicoes.getCookie())
			resultado = json.loads(resultado)['data'][0]
			id_video = resultado['id']
			tipo = 2
			nome = resultado['original_name']
			resultado = controlo.abrir_url(self.API_SITE+'aseguir.php?action=remover&tipo=anime&idVideo='+id_video, header=controlo.headers, cookie=definicoes.getCookie())
		resultado = json.loads(resultado)
		a_seguir = json.dumps(resultado['a_seguir'])
				
		controlo.escrever_ficheiro(os.path.join(controlo.pastaDados,'a_seguir.pobretv'), a_seguir)
		if resultado['mensagem']['codigo'] == 200:
			xbmc.executebuiltin("Notification(Pobre.tv,"+nome+": Deixado de seguir"+","+"6000"+","+ os.path.join(controlo.addonFolder,'icon.png')+")")
			xbmc.executebuiltin("Container.Refresh")

	def traktListas(self):
		url = 'https://api.trakt.tv/users/%s/lists' % controlo.addon.getSetting('utilizadorTrakt').replace('.', '-')
		listas = Trakt.getTraktAsJson(url)
		
		for s in json.loads(listas):
			controlo.addDir(s['name']+' ('+str(s['item_count'])+' items)', url+'/'+str(s['ids']['trakt'])+'/items', 'traktListasItems', os.path.join(controlo.artFolder, controlo.skin, 'trakt.png'))
		
		definicoes.vista_menu()

	def traktListasItems(self, url):
		lista = Trakt.getTraktAsJson(url)
		controlo.headers['Authorization'] = 'Bearer %s' % controlo.addon.getSetting('tokenPobretv')
		opcao = controlo.addon.getSetting('marcarVisto')
		for s in json.loads(lista):
			if s['type'] == 'movie':
				if s["movie"]["ids"]["imdb"] is None:
					continue
				imdb = s["movie"]["ids"]["imdb"]
				url = self.API_SITE+'filme/%s/imdb/qualidade/%s' % (imdb, definicoes.getQualidade())
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				resultado = json.loads(resultado)
				if 'codigo' in resultado:
					continue
				categoria = resultado['category1']
				if resultado['category2'] != '':
					categoria += ','+resultado['category2']
				if resultado['category3'] != '':
					categoria += ','+resultado['category3']
				
				pt = ''
				br = ''
				semLegenda = ''
				if resultado['legenda'] == "semlegenda":
					semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'

				if 'PT' in resultado['imdb']:
					resultado['imdb'] = re.compile('(.+?)PT').findall(resultado['imdb'].upper())[0]
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				visto = False
				if opcao == '1' or opcao == '2':
					if resultado['visto'] == 1:
						visto = True
				elif opcao == '0' or opcao == '2':
					visto = self.verificarVistoLocal(resultado['id_video'])
				infoLabels = {'Title': resultado['original_name'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'IMDBNumber': resultado['imdb'] }
				
				try:
					nome = resultado['original_name'].decode('utf-8')
				except:
					nome = resultado['original_name'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.API+'images/capas/'+resultado['foto'].split('/')[-1]
				if resultado['verdepois'] == 1:
					menuVerDepois = True
				else:
					menuVerDepois = False

				if resultado['favorito'] == 1:
					menuFavorito = True
				else:
					menuFavorito = False
				controlo.addVideo(pt+br+semLegenda+nome+' ('+resultado['ano']+')', self.API_SITE+'filme/'+str(resultado['id_video']), 'chooseStreamType', resultado['foto'],visto, 'filme', 0, 0, infoLabels, self.API+resultado['background'], trailer=resultado['trailer'], favorito=menuFavorito, agendado=menuVerDepois)
			elif s['type'] == 'show':
				if s["show"]["ids"]["imdb"] is None:
					continue
				imdb = s["show"]["ids"]["imdb"]
			
				
				url = self.API_SITE+'serie/%s/imdb' % (s["show"]["ids"]["imdb"] )
				resultado = controlo.abrir_url(url, header=controlo.headers)
				if resultado == 'DNS':
					controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
					return False
				tipo = 'serie'
				try:
					resultado = json.loads(resultado)
				except ValueError:
					continue
				if 'codigo' in resultado:
					url = self.API_SITE+'anime/%s/imdb' % (s["show"]["ids"]["imdb"] )
					resultado = controlo.abrir_url(url, header=controlo.headers)
					if resultado == 'DNS':
						controlo.alerta('Pobre.tv', 'Tem de alterar os DNS para poder usufruir do addon')
						return False
					tipo = 'anime'
					try:
						resultado = json.loads(resultado)
					except ValueError:
						continue
				if 'codigo' in resultado:
					continue
				

				categoria = resultado['category1']
				if resultado['category2'] != '':
					categoria += ','+resultado['category2']
				if resultado['category3'] != '':
					categoria += ','+resultado['category3']

				br = ''
				pt = ''
				if 'Brasileiro' in categoria:
					br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
				if 'Portu' in categoria:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				if 'PT' in resultado['imdb']:
					pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
				infoLabels = {'Title': resultado['original_name'], 'Year': resultado['ano'], 'Genre': categoria, 'Plot': resultado['descricao_video'], 'Cast':resultado['atores'].split(','), 'Trailer': resultado['trailer'], 'Director': resultado['diretor'], 'Rating': resultado['imdbRating'], 'Code': resultado['imdb'] }
			
				try:
					nome = resultado['original_name'].decode('utf-8')
				except:
					nome = resultado['original_name'].encode('utf-8')
				if 'http' not in resultado['foto']:
					resultado['foto'] = self.API+'images/capas/'+resultado['foto'].split('/')[-1]
				if resultado['visto'] == 1:
					visto=True
				else:
					visto=False
				if resultado['verdepois'] == 1:
					menuVerDepois = True
				else:
					menuVerDepois = False

				if resultado['favorito'] == 1:
					menuFavorito = True
				else:
					menuFavorito = False
				controlo.addDir(pt+br+nome+' ('+resultado['ano']+')', self.API_SITE+tipo+'/'+str(resultado['id_video']), 'temporadas', resultado['foto'], tipo='serie', infoLabels=infoLabels,poster=self.API+resultado['background'],visto=visto, menuO=True, favorito=menuFavorito, agendado=menuVerDepois)
		definicoes.vista_filmesSeries()

	def setFilme(self, i, vistos, opcao):
    
		categoria = definicoes.getCategoria(i['category1'])
		if int(i['category2']) != 0:
			categoria += ','+definicoes.getCategoria(i['category2'])
		if int(i['category3']) != 0:
			categoria += ','+definicoes.getCategoria(i['category3'])
		
		pt = ''
		br = ''
		semLegenda = ''
		imdbPT = False
		imdbBR = False
		
		try:
			if i['country'].upper() == 'BR':
				imdbBR = True
			elif i['country'].upper() == 'PT':
				imdbPT = True
		except:
			pass
		if i['subtitle'] == "semlegenda":
			semLegenda = '[COLOR red][B]S/ LEGENDA [/B][/COLOR]'
		if 'Brasileiro' in categoria or imdbBR == True:
			br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
		if 'Portu' in categoria or imdbPT == True or 'PT' in i['imdb'].upper():
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		cor = "white"
		if 'PT' in i['imdb'].upper():
			i['imdb'] = re.compile('(.+?)PT').findall(i['imdb'].upper())[0]

		visto = False
		vistoa = False
		if opcao == '1' or opcao == '2':
			if self.getVistoFilme(i['id']) == True:
				vistoa = True
		elif opcao == '0' or opcao == '2':
			vistoa = self.verificarVistoLocal(i['id'])
		
		if Trakt.loggedIn():
			
			for v in json.loads(vistos):
			
				if v["movie"]["ids"]["imdb"] is None:
					continue
				if v["movie"]["ids"]["imdb"].upper() == i['imdb'].upper() or v["movie"]["ids"]["imdb"]+'PT'.upper() == i['imdb']+'PT'.upper():
					visto = True
					cor = "blue"
					break
				else:
					visto = False
		if vistoa or visto:
			visto = True
		else:
			visto = False
		try:
			nome = i['original_name'].decode('utf-8')
		except:
			nome = i['original_name'].encode('utf-8')
		if 'http' not in i['poster']:
			i['poster'] = self.API+'images/capas/'+i['poster'].split('/')[-1]

		menuVerDepois = self.getVerDepois(i['id'], 'm')
		menuASeguir = self.getASeguir(i['id'], 'm')
		menuFavorito = self.getFavoritos(i['id'], 'm')
		url = self.API_SITE+'filmes.php?action='+str(i['id'])
		infoLabels = {'Title': i['original_name'], 'Year': i['release_year'], 'Genre': categoria, 'Plot':i['synopsis'], 'Cast': [], 'Trailer': i['trailer'], 'Director': '', 'Rating': i['rating'], 'IMDBNumber': i['imdb'] }
		try:
			nome = nome.decode('utf-8')
		except:
			nome = str(nome)

		fullname = '[COLOR '+cor+']'+pt+br+semLegenda+nome+' ('+str(i['release_year'])+')[/COLOR]'
		controlo.addVideo(fullname, self.API_SITE+'filmes.php?action=id&idFilme='+str(i['id']), 'chooseStreamType', i['poster'],visto, 'filme', 0, 0, infoLabels, i['background'], trailer=i['trailer'], favorito=menuFavorito, agendado=menuVerDepois, aseguir=menuASeguir)

	def setSeries(self, i, vistos, opcao, tipo):
			
		categoria = definicoes.getCategoria(i['category1'])
		if int(i['category2']) != 0:
			categoria += ','+definicoes.getCategoria(i['category2'])
		if int(i['category3']) != 0:
			categoria += ','+definicoes.getCategoria(i['category3'])
		
		pt = ''
		br = ''
		semLegenda = ''
		imdbPT = False
		imdbBR = False
		
		try:
			if i['country'].upper() == 'BR':
				imdbBR = True
			elif i['country'].upper() == 'PT':
				imdbPT = True
		except:
			pass
		if 'Brasileiro' in categoria or imdbBR == True:
			br = '[B][COLOR green]B[/COLOR][COLOR yellow]R[/COLOR]: [/B]'
		if 'Portu' in categoria or imdbPT == True or 'PT' in i['imdb'].upper():
			pt = '[B][COLOR green]P[/COLOR][COLOR red]T[/COLOR]: [/B]'
		cor = "white"
		if 'PT' in i['imdb'].upper():
			i['imdb'] = re.compile('(.+?)PT').findall(i['imdb'].upper())[0]

		visto = False
		vistoa = False
		if opcao == '1' or opcao == '2':
			if self.getVistoFilme(i['id']) == True:
				vistoa = True
		elif opcao == '0' or opcao == '2':
			vistoa = self.verificarVistoLocal(i['id'])
		if vistoa:
			visto = True
		else:
			visto = False
		try:
			nome = i['original_name'].decode('utf-8')
		except:
			nome = i['original_name'].encode('utf-8')
		if 'http' not in i['poster']:
			i['poster'] = self.API+'images/capas/'+i['poster'].split('/')[-1]
		
		menuVerDepois = self.getVerDepois(i['id'], 't')
		menuASeguir = self.getASeguir(i['id'], 't')
		menuFavorito = self.getFavoritos(i['id'], 't')
		try:
			nome = nome.decode('utf-8')
		except:
			nome = str(nome)
		infoLabels = {'Title': i['original_name'], 'Year': i['release_year'], 'Genre': categoria, 'Plot': i['synopsis'], 'Cast': [], 'Trailer': i['trailer'], 'Director': '', 'Rating': i['rating'], 'Code': i['imdb'] }
		fullname = pt+br+nome+' ('+i['release_year']+')'
		controlo.addDir(fullname, self.API_SITE+tipo+'.php?action=id&idSerie='+str(i['id']), 'temporadas', i['poster'], tipo='serie', infoLabels=infoLabels,poster=i['background'],visto=visto, menuO=True, favorito=menuFavorito, agendado=menuVerDepois, aseguir=menuASeguir)
	def slugify(value, allow_unicode=False):
		value = str(value)
		if allow_unicode:
			value = unicodedata.normalize('NFKC', value)
		else:
			value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
		value = re.sub(r'[^\w\s-]', '', value.lower())
		return str(re.sub(r'[-\s]+', '-', value).strip('-_'))

	def setPagination(self, current, total, proximo, local):
		
		currentAux = int(current)+1

		if int(current) < int(total):
			controlo.addDir('Próxima página ('+str(current)+'/'+str(total)+')', proximo, local, os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
			pagina100 = int(current)
			pagina10 = int(current)

			if((int(current) + 10) < int(total)):
				pagina10 = (int(current) + 10)
			else:
				pagina10 = total
			if pagina10 != current and pagina10 != total:
				proximo10 = proximo.replace('page='+str(currentAux), 'page='+str(pagina10))
				controlo.addDir('Ir para a página '+str(pagina10), proximo10, local, os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))

			if((int(current) + 100) < int(total)):
				pagina100 = (int(current) + 100)
			else:
				pagina100 = total
			if pagina100 != current and pagina100 != total:
				proximo100 = proximo.replace('page='+str(currentAux), 'page='+str(pagina100))
				controlo.addDir('Ir para a página '+str(pagina100), proximo100, local, os.path.join(controlo.artFolder, controlo.skin, 'proximo.png'))
