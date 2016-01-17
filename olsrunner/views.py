from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from cassiopeia import riotapi, baseriotapi
from cassiopeia.dto import tournamentproviderapi
from cassiopeia.type.core.common import SubType
from olsrunner.models import Player, Game, Team, Stats, Week, TourneyCode
from django.template import loader, Context
from django.contrib.auth.decorators import permission_required
from django.core import serializers
from django.db.models import Max, Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import date, time, timedelta, datetime
from django.db import connection
import pickle
import json

def index(request):
	return HttpResponse(render(request, 'index.html',))
# Create your views here.

class Match:
	pass


#                                                                           ADMIN VIEWS




@permission_required('ols.olsadmin')
def addPlayers(request):
	#for row in Player.objects.all():
	#	if Player.objects.filter(SummonerNumber=row.SummonerNumber).count() > 1:
	#		row.delete()
	return HttpResponse(render(request, 'addplayers.html', ))

@permission_required('ols.olsadmin')
def addplayerlist(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/ols/login')
	else:
		posted = request.POST
		#playerlist = posted.split(','')
		playerlist = posted.get('players').split(',')
		print(playerlist)
		riotapi.set_region("NA")
		for player in playerlist:
			player = player.split(':')
			play = Player()		
			play.PlayerName = player[0]
			play.PlayerIGN = player[1]
			play.SummonerNumber = riotapi.get_summoner_by_name(player[1]).id
			play.save()
		return HttpResponse("Added players")

@permission_required('ols.olsadmin')
def AddTeam(request):
	if request.POST:
		newteam = Team()
		posted = request.POST
		#print(posted.get('teamname'))
		newteam.teamName = posted.get('teamname')
		newteam.Captain = posted.get('cap')
		newteam.Player1 = posted.get('P1')
		newteam.Player2 = posted.get('P2')
		newteam.Player3 = posted.get('P3')
		newteam.Player4 = posted.get('P4')
		riotapi.set_region("NA")
		summtoadd = riotapi.get_summoner_by_name(newteam.Captain)
		print(summtoadd)
		newteam.CaptainID = summtoadd.id
		summtoadd = riotapi.get_summoner_by_name(newteam.Player1)
		print(summtoadd)
		newteam.Player1ID = summtoadd.id
		summtoadd = riotapi.get_summoner_by_name(newteam.Player2)
		print(summtoadd)
		newteam.Player2ID = summtoadd.id
		summtoadd = riotapi.get_summoner_by_name(newteam.Player3)
		print(summtoadd)
		newteam.Player3ID = summtoadd.id
		summtoadd = riotapi.get_summoner_by_name(newteam.Player4)
		print(summtoadd)
		newteam.Player4ID = summtoadd.id
		#print(Team.objects.all().aggregate(Max('teamID')))
		try:
			if Team.objects.all().aggregate(Max('teamID'))['teamID_max'] is not None:
				newteam.teamID = Team.objects.all().aggregate(Max('teamID'))['teamID__max'] + 1
			else:
				raise KeyError("no teams yet")
		except KeyError:
			newteam.teamID = 0
		newteam.save()
		return HttpResponse(render(request, 'addedteam.html'))
	else:
		return HttpResponse(render(request, 'addteam.html'))


def addPoints(winner, loser, winnerpos):
	winner.points = winner.points + 1
	if winnerpos == 1:
		gm = Game.objects.filter(team1__iexact= loser.teamID)
		try:
			gm = gm.objects.get(team2__iexact= winner.teamID)
		except ObjectDoesNotExist:
			winner.save()
			return
	else:
		gm = Game.objects.filter(team2__iexact=loser.teamID)
		try:
			gm = gm.objects.get(team1__iexact=winner.teamID)
		except ObjectDoesNotExist:
			winner.save()
			return
	winner.points = winner.points + 1
	winner.save()
	return
@permission_required('ols.olsadmin')
def addMatch(request):
	if request.POST:
		newgame = Game()
		posted = request.POST
		print(posted.get('team1name'))
		newgame.team1 = Team.objects.get(teamName__iexact=posted.get('team1name')).teamID
		newgame.team2 = Team.objects.get(teamName__iexact=posted.get('team2name')).teamID
		newgame.winner = Team.objects.get(teamName__iexact=posted.get('winner')).teamID
		try:
			newgame.Number = Game.objects.all().aggregate(Max('Number'))['Number'] + 1
		except KeyError:
			newgame.Number = 0
		riotapi.set_region("NA")
		m = riotapi.get_match(posted.get('match'))
		if newgame.team2 == newgame.winner:
			loser = Team.objects.get(teamName__iexact=posted.get('team1name'))
			position = 2
		else:
			loser = Team.objects.get(teamName__iexact=posted.get('team2name'))
			position = 1
		addPoints(Team.objects.get(teamName__iexact=posted.get('winner')), loser, position)
		print(posted.get('P2'))
		namelist= []
		namelist.append(posted.get('P1'))
		namelist.append(posted.get('P2'))
		namelist.append(posted.get('P3'))
		namelist.append(posted.get('P4'))
		namelist.append(posted.get('P5'))
		namelist.append(posted.get('2P1'))
		namelist.append(posted.get('2P2'))
		namelist.append(posted.get('2P3'))
		namelist.append(posted.get('2P4'))
		namelist.append(posted.get('2P5'))
		summoners = riotapi.get_summoners_by_name(namelist)
		print(dir(summoners[0]))
		print(summoners[0].id)
		newgame.team1Player1 = summoners[0].id
		newgame.team1Player2 = summoners[1].id
		newgame.team1Player3 = summoners[2].id
		newgame.team1Player4 = summoners[3].id
		newgame.team1Player5 = summoners[4].id
		newgame.team2Player1 = summoners[5].id
		newgame.team2Player2 = summoners[6].id
		newgame.team2Player3 = summoners[7].id
		newgame.team2Player4 = summoners[8].id
		newgame.team2Player5 = summoners[9].id
		newgame.matchID = posted.get('match')
		i = 0
		for player in m.participants:
			try:
				st = Stats.objects.get(PlayerID=summoners[i].id)
			except:
				st = Stats()
				st.PlayerID = summoners[i].id
			i= i+ 1
			st.Kills = st.Kills + player.stats.kills
			st.Deaths = st.Deaths + player.stats.deaths
			st.Assists = st.Assists + player.stats.assists
			st.GoldTotal = st.GoldTotal + player.stats.gold_earned
			st.GamesPlayed = st.GamesPlayed + 1
			if player.stats.largest_critical_strike > st.LargestCrit:
				st.LargestCrit = player.stats.largest_critical_strike
			st.Creeps = st.Creeps + player.stats.minion_kills + player.stats.monster_kills
			st.SecondsPlayed = st.SecondsPlayed + m.duration.total_seconds()/60
			st.save()
		with open('olsrunner/matches/' + str(newgame.Number) + '.pk', 'wb') as outfile:
			pickle.dump( m , outfile)
		newgame.filename = 'olsrunner/matches/' + str(newgame.Number) + '.pk'
		newgame.save()
		return HttpResponse("match added")
	else:
		teamNames = []
		teams = Team.objects.all().values('teamName')
		for t in teams:
			teamNames.append(t['teamName'])
		
		return HttpResponse(render(request, 'addMatch.html', {'teams' :teamNames}))

@permission_required('ols.olsadmin')
def updateIDs(request):
	NoIDs = Player.objects.filter(SummonerNumber=0)
	riotapi.set_region("NA")
	for play in NoIDs:
		summtoadd = riotapi.get_summoner_by_name(play.PlayerIGN)
		play.SummonerNumber = summtoadd.id
		play.save()
		print(summtoadd.id)
	return HttpResponse("All unset IDs have been updated")

@permission_required('ols.olsadmin')
def updateTeamIDs(request):
	teams = Team.objects.all()
	riotapi.set_region("NA")
	for t in teams:
		if t.CaptainID == 0:
			summtoadd = riotapi.get_summoner_by_name(t.Captain)
			t.CaptainID = summtoadd.id
		if t.Player1ID == 0:
			summtoadd = riotapi.get_summoner_by_name(t.Player1)
			t.Player1ID = summtoadd.id
		if t.Player2ID == 0:
			summtoadd = riotapi.get_summoner_by_name(t.Player2)
			t.Player2ID = summtoadd.id
		if t.Player3ID == 0:
			summtoadd = riotapi.get_summoner_by_name(t.Player3)
			t.Player3ID = summtoadd.id
		if t.Player4ID == 0:
			summtoadd = riotapi.get_summoner_by_name(t.Player4)
			t.Player4ID = summtoadd.id
		t.save()

	return HttpResponse("All unset IDs have been updated")

@permission_required('ols.olsadmin')
def generatecodes(request):
	#6365 is spring tournament ID
	baseriotapi.set_region("NA")
	weeks = 5
	gamesperweek = 12
	codecount = weeks * gamesperweek * 2
	codes = baseriotapi.create_tournament_codes(6365, count=codecount)
	i = 0
	weekcount = 0
	for week in Week.objects.all():
		savecode = TourneyCode()
		savecode.team1 =  week.L0game1t1
		savecode.team2 =  week.L0game1t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 0
		savecode.game = 1
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()
		savecode.team1 =  week.L0game1t1
		savecode.team2 =  week.L0game1t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 0
		savecode.game = 1
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L0game2t1
		savecode.team2 =  week.L0game2t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 0
		savecode.game = 2
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L0game2t1
		savecode.team2 =  week.L0game2t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 0
		savecode.game = 2
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L0game3t1
		savecode.team2 =  week.L0game3t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 0
		savecode.game = 3
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L0game3t1
		savecode.team2 =  week.L0game3t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 0
		savecode.game = 3
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L1game1t1
		savecode.team2 =  week.L1game1t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 1
		savecode.game = 1
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L1game1t1
		savecode.team2 =  week.L1game1t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 1
		savecode.game = 1
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L1game2t1
		savecode.team2 =  week.L1game2t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 1
		savecode.game = 2
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L1game2t1
		savecode.team2 =  week.L1game2t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 1
		savecode.game = 2
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L1game3t1
		savecode.team2 =  week.L1game3t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 1
		savecode.game = 3
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L1game3t1
		savecode.team2 =  week.L1game3t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 1
		savecode.game = 3
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L2game1t1
		savecode.team2 =  week.L2game1t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 2
		savecode.game = 1
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L2game1t1
		savecode.team2 =  week.L2game1t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 2
		savecode.game = 1
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L2game2t1
		savecode.team2 =  week.L2game2t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 2
		savecode.game = 2
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L2game2t1
		savecode.team2 =  week.L2game2t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 2
		savecode.game = 2
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L2game3t1
		savecode.team2 =  week.L2game3t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 2
		savecode.game = 3
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L2game3t1
		savecode.team2 =  week.L2game3t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 2
		savecode.game = 3
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L3game1t1
		savecode.team2 =  week.L3game1t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 3
		savecode.game = 1
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L3game1t1
		savecode.team2 =  week.L3game1t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 3
		savecode.game = 1
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L3game2t1
		savecode.team2 =  week.L3game2t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 3
		savecode.game = 2
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L3game2t1
		savecode.team2 =  week.L3game2t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 3
		savecode.game = 2
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L3game3t1
		savecode.team2 =  week.L3game3t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 3
		savecode.game = 3
		savecode.rift = 0
		savecode.save()
		i = i + 1
		savecode = TourneyCode()

		savecode.team1 =  week.L3game3t1
		savecode.team2 =  week.L3game3t2
		savecode.code = codes[i]
		savecode.week = weekcount
		savecode.league = 3
		savecode.game = 3
		savecode.rift = 1
		savecode.save()
		i = i + 1
		savecode = TourneyCode()
		weekcount = weekcount + 1

  #                                                       CAPTAIN VIEWS




def callback(request):
	posted = request.POST
	print(posted)
	gameparse = json.loads(posted[0])
	print(gameparse['winningTeam'])
	newgame = Game()
	code = TourneyCode.objects.get(code = gameparse['shortCode'])
	newgame.team1 = code.team1
	team1obj = Team.objects.get(teamID = newgame.team1)
	newgame.team2 = code.team2
	team2obj = Team.objects.get(teamID = newgame.team1)
	for p in gameparse['winningTeam']:
		if p.summonerId  == team1obj.CaptainID:
			newgame.winner = newgame.team1
			break
		if p.summonerId  == team1obj.Player1ID:
			newgame.winner = newgame.team1
			break
		if p.summonerId  == team1obj.Player2ID:
			newgame.winner = newgame.team1
			break
		if p.summonerId  == team1obj.Player3ID:
			newgame.winner = newgame.team1
			break
		if p.summonerId  == team1obj.Player4ID:
			newgame.winner = newgame.team1
			break
		if p.summonerId  == team2obj.CaptainID:
			newgame.winner = newgame.team2
			break
		if p.summonerId  == team2obj.Player1ID:
			newgame.winner = newgame.team2
			break
		if p.summonerId  == team2obj.Player2ID:
			newgame.winner = newgame.team2
			break
		if p.summonerId  == team2obj.Player3ID:
			newgame.winner = newgame.team2
			break
		if p.summonerId  == team2obj.Player4ID:
			newgame.winner = newgame.team2
			break
	try:
		newgame.Number = Game.objects.all().aggregate(Max('Number'))['Number'] + 1
	except KeyError:
		newgame.Number = 0
	if newgame.team2 == newgame.winner:
		loser = team1obj
		winer = team2obj
		position = 2
	else:
		winner = team1obj
		loser = team2obj
		position = 1
	addPoints(winner, loser, position)
	if position == 1:
		newgame.team1Player1 = gameparse['winningTeam'][0]
		newgame.team1Player2 = gameparse['winningTeam'][1]
		newgame.team1Player3 = gameparse['winningTeam'][2]
		newgame.team1Player4 = gameparse['winningTeam'][3]
		newgame.team1Player5 = gameparse['winningTeam'][4]
		newgame.team2Player1 = gameparse['losingTeam'][0]
		newgame.team2Player2 = gameparse['losingTeam'][1]
		newgame.team2Player3 = gameparse['losingTeam'][2]
		newgame.team2Player4 = gameparse['losingTeam'][3]
		newgame.team2Player5 = gameparse['losingTeam'][4]
	else:
		newgame.team1Player1 = gameparse['losingTeam'][0]
		newgame.team1Player2 = gameparse['losingTeam'][1]
		newgame.team1Player3 = gameparse['losingTeam'][2]
		newgame.team1Player4 = gameparse['losingTeam'][3]
		newgame.team1Player5 = gameparse['losingTeam'][4]
		newgame.team2Player1 = gameparse['winningTeam'][0]
		newgame.team2Player2 = gameparse['winningTeam'][1]
		newgame.team2Player3 = gameparse['winningTeam'][2]
		newgame.team2Player4 = gameparse['winningTeam'][3]
		newgame.team2Player5 = gameparse['winningTeam'][4]
	
	newgame.matchID = gameparse['gameId']
	i = 0
	riotapi.set_region("NA")
	m = riotapi.get_match(gameparse['id'], True, tournament_code=gameparse['shortCode'])
	for player in m.participants:
		try:
			st = Stats.objects.get(PlayerID=player.id)
		except:
			st = Stats()
			st.PlayerID = player.id 
		i= i+ 1
		st.Kills = st.Kills + player.stats.kills
		st.Deaths = st.Deaths + player.stats.deaths
		st.Assists = st.Assists + player.stats.assists
		st.GoldTotal = st.GoldTotal + player.stats.gold_earned
		st.GamesPlayed = st.GamesPlayed + 1
		if player.stats.largest_critical_strike > st.LargestCrit:
			st.LargestCrit = player.stats.largest_critical_strike
		st.Creeps = st.Creeps + player.stats.minion_kills + player.stats.monster_kills
		st.SecondsPlayed = st.SecondsPlayed + m.duration.total_seconds()/60
		st.save()
	with open('olsrunner/matches/' + str(newgame.Number) + '.pk', 'wb') as outfile:
		pickle.dump( m , outfile)
	newgame.filename = 'olsrunner/matches/' + str(newgame.Number) + '.pk'
	newgame.save()
	return HttpResponse("match added")


def reschedule(request):
	posted = request.POST
	match = posted['match']
	matchs = match.split('|')
	weeks = Week.objects.all().order_by('startdate')
	print(weeks)
	try:
		dateof = datetime.strptime(posted['date'], '%m/%d/%Y')
	except ValueError:
		dateof = datetime.strptime(posted['date'], '%b. %d, %Y')
	try:
		timeof = datetime.strptime(posted['time'], '%I:%M a.m.')

	except ValueError:
		timeof = datetime.strptime(posted['time'], '%I:%M p.m.')
		timeof = timeof +timedelta(hours=12)
	#timeof = timeof.strftime('%H:%M:%S')
	#timeof = timeof.time
	#dateof = dateof.strftime('%Y-%m-%d')
	#dateof = dateof.date
	week = weeks[int(matchs[0])-1] #this gets the week list
	if week.L0game1t1==int(matchs[1]): #if team1 matches
		week.L0game1Time = timeof
		week.L0game1date = dateof
	if week.L0game2t1==int(matchs[1]):
		week.L0game2Time = timeof
		week.L0game2date = dateof
	if week.L0game3t1==int(matchs[1]):
		week.L0game3Time = timeof
		week.L0game3date = dateof
	if week.L1game1t1==int(matchs[1]):
		week.L1game1Time = timeof
		week.L1game1date = dateof
	if week.L1game2t1==int(matchs[1]):
		week.L1game2Time = timeof
		week.L1game2date = dateof
	if week.L1game3t1==int(matchs[1]):
		week.L1game3Time = timeof
		week.L1game3date = dateof
	if week.L2game1t1==int(matchs[1]):
		week.L2game1Time = timeof
		week.L2game1date = dateof
	if week.L2game2t1==int(matchs[1]):
		week.L2game2Time = timeof
		week.L2game2date = dateof
	if week.L2game3t1==int(matchs[1]):
		week.L2game3Time = timeof
		week.L2game3date = dateof
	if week.L3game1t1==int(matchs[1]):
		week.L0game1Time = timeof
		week.L0game1date = dateof
	if week.L3game2t1==int(matchs[1]):
		week.L3game2Time = timeof
		week.L3game2date = dateof
	if week.L3game3t1==int(matchs[1]):
		week.L3game3Time = timeof
		week.L3game3date = dateof
	print("final check")
	#import pdb; pdb.set_trace()
	week.save()
	print(connection.queries)
	return HttpResponseRedirect('/ols/schedule')



		#                                                     GENERAL VIEWS

def overallstats(request):
	return HttpResponse("Error 404 <3 Matt")


def player_stats(request, player):
	print(player)
	shit = False
	try:
		play = Player.objects.get(SummonerNumber=player)
	except ValueError:
		print('player link with IGN')
		shit = True
	if shit:	
		try:
			play = Player.objects.get(PlayerIGN__icontains=player)
		except ObjectDoesNotExist:
			try:
				play = Player.objects.get(PlayerName__icontains=player)
			except ObjectDoesNotExist:
					return HttpResponse("Player not found")
		except MultipleObjectsReturned:	
			try:
				play = Player.objects.get(PlayerName__icontains=player)
			except ObjectDoesNotExist:
				return HttpResponse("Your search was too general, multiple players found")
			except MultipleObjectsReturned:	
				return HttpResponse("Your search was too general, multiple players found")
	
	try:
		s = Stats.objects.get(PlayerID=play.SummonerNumber)
	except KeyError:
		return HttpResponse("No stats for this player yet")
	except ObjectDoesNotExist:
		return HttpResponse("No stats for this player yet")

	query = Q(team1Player1= play.SummonerNumber) | Q(team1Player2= play.SummonerNumber) | Q(team1Player3= play.SummonerNumber) | Q(team1Player4= play.SummonerNumber) | Q(team1Player5= play.SummonerNumber) | Q(team2Player1= play.SummonerNumber) | Q(team2Player2= play.SummonerNumber) | Q(team2Player3= play.SummonerNumber) |Q(team2Player4= play.SummonerNumber) | Q(team2Player5= play.SummonerNumber)
	g = Game.objects.filter(query)
	gm = []
	for game in g:
		if game.team1Player1 ==play.SummonerNumber:
			i = 0
		if game.team1Player2 ==play.SummonerNumber:
			i =1
		if game.team1Player3 ==play.SummonerNumber:
			i=2
		if game.team1Player4 ==play.SummonerNumber:
			i=3
		if game.team1Player5 ==play.SummonerNumber:
			i=4
		if game.team2Player1 ==play.SummonerNumber:
			i=5
		if game.team2Player2 ==play.SummonerNumber:
			i=6
		if game.team2Player3 ==play.SummonerNumber:
			i=7
		if game.team2Player4 ==play.SummonerNumber:
			i=8
		if game.team2Player5 ==play.SummonerNumber:
			i=9
		with open(str(game.filename), 'rb') as infile:
			gamefile = pickle.load(infile)	
		gm.append({'game': game, 'player':gamefile.participants[i], 'name':str(game)})

	tquery = Q(CaptainID=play.SummonerNumber) | Q(Player1ID=play.SummonerNumber) |  Q(Player2ID=play.SummonerNumber) |  Q(Player3ID=play.SummonerNumber) |  Q(Player4ID=play.SummonerNumber)
	t = Team.objects.get(tquery)
	advancedstats = {}
	advancedstats['KDA'] = (s.Kills + s.Assists) / s.Deaths
	advancedstats['Csmin'] = s.Creeps / s.SecondsPlayed
	advancedstats['GPM'] = s.GoldTotal / s.SecondsPlayed

	return HttpResponse(render(request, 'playerStats.html', {'player' :play, 'stats': s, 'team': t, 'games': gm, 'astats':advancedstats} ))


def team_stats(request, team):
	t = Team.objects.get(teamID=team)
	blank = Stats()
	players = []
	stats = []
	p1 = Player.objects.get(SummonerNumber=t.CaptainID)
	try:
		print(p1)
		p1s = Stats.objects.get(PlayerID=p1.SummonerNumber)
		print(p1)
	except KeyError:
		p1s = blank
	except ObjectDoesNotExist:
		p1s = blank
	players.append(p1)

	stats.append(p1s)
	print(players)
	p2 = Player.objects.get(SummonerNumber=t.Player1ID)
	print(p2)
	try:
		p2s = Stats.objects.get(PlayerID=p2.SummonerNumber)
	except KeyError:
		p2s = blank
	except ObjectDoesNotExist:
		p2s = blank
	players.append(p2)
	print(players)
	stats.append(p2s)
	p3 = Player.objects.get(SummonerNumber=t.Player2ID)
	try:
		p3s = Stats.objects.get(PlayerID=p3.SummonerNumber)
	except KeyError:
		p3s = blank
	except ObjectDoesNotExist:
		p3s = blank
	players.append(p3)
	print(players)
	stats.append(p3s)
	p4 = Player.objects.get(SummonerNumber=t.Player3ID)
	try:
		p4s = Stats.objects.get(PlayerID=p4.SummonerNumber)
	except KeyError:
		p4s = blank
	except ObjectDoesNotExist:
		p4s = blank
	players.append(p4)
	print(players)
	stats.append(p4s)
	p5 = Player.objects.get(SummonerNumber=t.Player4ID)
	try:
		p5s = Stats.objects.get(PlayerID=p1.SummonerNumber)
	except KeyError:
		p5s = blank
	except ObjectDoesNotExist:
		p5s = blank
	players.append(p5)
	stats.append(p5s)
	print(players)
	teamavgs = {}
	games = Game.objects.filter(Q(team1=t.teamID) | Q(team2 = t.teamID)) 
	gameslist= []
	for g in games:
		team1 = Team.objects.get(teamID= g.team1)
		team2 = Team.objects.get(teamID= g.team2)
		if g.winner == t.teamID:
			win = "Won"
		else:
			win = "Lose"
		teaminfo ={"t1": team1, "t2":team2, "won": win, "game": g}
		print(teaminfo)
		gameslist.append(teaminfo)
	print(t.teamName)
	return HttpResponse(render(request, 'teamStats.html', {'p' :players, 's': stats, 't': t, 'gs': gameslist} ))
def match(request, match_num):
	try:
		m = Game.objects.get(Number=match_num)
	except ObjectDoesNotExist:
		return HttpResponse("There is no match with this ID")
	with open(str(m.filename), 'rb') as infile:
		game = pickle.load(infile)
	#name = str(m)
	riotapi.set_region("NA")
	team1 = []
	try:
		team1.append(Player.objects.get(SummonerNumber=m.team1Player1))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team1Player1
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team1Player1)
		team1.append(sub)

	try:
		team1.append(Player.objects.get(SummonerNumber=m.team1Player2))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team1Player2
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team1Player2)
		team1.append(sub)
	try:	
		team1.append(Player.objects.get(SummonerNumber=m.team1Player3))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team1Player3
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team1Player3)
		team1.append(sub)
	try:
		team1.append(Player.objects.get(SummonerNumber=m.team1Player4))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team1Player4
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team1Player4)
		team1.append(sub)
	try:	
		team1.append(Player.objects.get(SummonerNumber=m.team1Player5))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team1Player5
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team1Player5)
		team1.append(sub)
	team2 = []
	try:
		team2.append(Player.objects.get(SummonerNumber=m.team2Player1))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team2Player1
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team2Player1)
		team2.append(sub)
	try:
		team2.append(Player.objects.get(SummonerNumber=m.team2Player2))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team2Player2
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team2Player2)
		team2.append(sub)
	try:	
		team2.append(Player.objects.get(SummonerNumber=m.team2Player3))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team2Player3
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team2Player3)
		team2.append(sub)
	try:	
		team2.append(Player.objects.get(SummonerNumber=m.team2Player4))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team2Player4
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team2Player4)
		team2.append(sub)
	try:	
		team2.append(Player.objects.get(SummonerNumber=m.team2Player5))
	except ObjectDoesNotExist:
		sub = Player()
		sub.SummonerNumber = m.team2Player5
		sub.PlayerIGN = riotapi.get_summoner_by_id(m.team2Player5)
		team2.append(sub)
	return HttpResponse(render(request, 'Match.html', {'matchinfo' :m, 'game' : game, 't1': team1, 't2': team2}))

def standings(request):
	teamsbyleague= {}
	teamsbyleague['Demacia'] = Team.objects.filter(league=0).order_by('-points')
	teamsbyleague['Noxus'] = Team.objects.filter(league=1).order_by('-points')
	teamsbyleague['Piltover'] = Team.objects.filter(league=2).order_by('-points')
	teamsbyleague['Ionia'] = Team.objects.filter(league=3).order_by('-points')
	return HttpResponse(render(request, 'standings.html', {'leagues': teamsbyleague} ))

def schedule(request):
	#return HttpResponse("Tournament code testing right now")
	schedule = []
	weeks = []
	weeks = Week.objects.all().order_by('startdate')
	i = 0
	for w in weeks:
		wk = {}
		wkl0= []
		wkl0.append({'team1': Team.objects.get(teamID=w.L0game1t1), 'team2': Team.objects.get(teamID=w.L0game1t2), 'time' : w.L0game1Time, 'canedit' : False, 'date' :w.L0game1date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=0).filter(game=1).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=0).filter(game=1).get(rift=1)})
		wkl0.append({'team1': Team.objects.get(teamID=w.L0game2t1), 'team2': Team.objects.get(teamID=w.L0game2t2), 'time' : w.L0game2Time, 'canedit' : False, 'date' :w.L0game2date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=0).filter(game=2).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=0).filter(game=2).get(rift=1)})
		wkl0.append({'team1': Team.objects.get(teamID=w.L0game3t1), 'team2': Team.objects.get(teamID=w.L0game3t2), 'time' : w.L0game3Time, 'canedit' : False, 'date' :w.L0game3date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=0).filter(game=3).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=0).filter(game=3).get(rift=1)})
		wk['Demacia'] = wkl0
		wkl1= []
		wkl1.append({'team1': Team.objects.get(teamID=w.L1game1t1), 'team2': Team.objects.get(teamID=w.L1game1t2), 'time' : w.L1game1Time, 'canedit' : False, 'date' :w.L1game1date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=1).filter(game=1).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=1).filter(game=1).get(rift=1)})
		wkl1.append({'team1': Team.objects.get(teamID=w.L1game2t1), 'team2': Team.objects.get(teamID=w.L1game2t2), 'time' : w.L1game2Time, 'canedit' : False, 'date' :w.L1game2date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=1).filter(game=2).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=1).filter(game=2).get(rift=1)})
		wkl1.append({'team1': Team.objects.get(teamID=w.L1game3t1), 'team2': Team.objects.get(teamID=w.L1game3t2), 'time' : w.L1game3Time, 'canedit' : False, 'date' :w.L1game3date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=1).filter(game=3).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=1).filter(game=3).get(rift=1)})
		wk['Noxus'] = wkl1
		wkl2= []
		wkl2.append({'team1': Team.objects.get(teamID=w.L2game1t1), 'team2': Team.objects.get(teamID=w.L2game1t2), 'time' : w.L2game1Time, 'canedit' : False, 'date' :w.L2game1date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=2).filter(game=1).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=2).filter(game=1).get(rift=1)})
		wkl2.append({'team1': Team.objects.get(teamID=w.L2game2t1), 'team2': Team.objects.get(teamID=w.L2game2t2), 'time' : w.L2game2Time, 'canedit' : False, 'date' :w.L2game2date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=2).filter(game=2).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=2).filter(game=2).get(rift=1)})
		wkl2.append({'team1': Team.objects.get(teamID=w.L2game3t1), 'team2': Team.objects.get(teamID=w.L2game3t2), 'time' : w.L2game3Time, 'canedit' : False, 'date' :w.L2game3date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=2).filter(game=3).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=2).filter(game=3).get(rift=1)})
		wk['Piltover'] =wkl2
		wkl3= []
		wkl3.append({'team1': Team.objects.get(teamID=w.L3game1t1), 'team2': Team.objects.get(teamID=w.L3game1t2), 'time' : w.L3game1Time, 'canedit' : False, 'date' :w.L3game1date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=3).filter(game=1).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=3).filter(game=1).get(rift=1)})
		wkl3.append({'team1': Team.objects.get(teamID=w.L3game2t1), 'team2': Team.objects.get(teamID=w.L3game2t2), 'time' : w.L3game2Time, 'canedit' : False, 'date' :w.L3game2date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=3).filter(game=2).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=3).filter(game=2).get(rift=1)})
		wkl3.append({'team1': Team.objects.get(teamID=w.L3game3t1), 'team2': Team.objects.get(teamID=w.L3game3t2), 'time' : w.L3game3Time, 'canedit' : False, 'date' :w.L3game3date, 'game1code':  TourneyCode.objects.filter(week=i).filter(league=3).filter(game=3).get(rift=0)  , 'game2code': TourneyCode.objects.filter(week=i).filter(league=3).filter(game=3).get(rift=1)})
		wk['Ionia'] = wkl3

		#Captain namechanges will not work correctly currently
		try:
			if request.user.is_authenticated():
				cap = Player.objects.get(username = request.user.username)
				team2edit = Team.objects.get(CaptainID = cap.SummonerNumber)
				if team2edit.league == 0:
					l = 'Demacia'
				if team2edit.league == 1:
					l = 'Noxus'
				if team2edit.league == 2:
					l = 'Piltover'
				if team2edit.league == 3:
					l = 'Ionia'	
				for game in wk[l]:
					#print(game)
					if game['team1'] == team2edit:
						game['canedit'] = True
					if game['team2'] == team2edit:
						game['canedit'] = True	
		except ObjectDoesNotExist:
			print("not a captain")
		schedule.append({'startdate': w.startdate, 'week': wk})
		#print(wk['Demacia'][0])
		#print(schedule)
		#print(schedule[0])
		#print(schedule[0][w.startdate]['Demacia'])
		#print(str(w.L0game2date.ctime()))
		i = i+1
	return HttpResponse(render(request, 'schedule.html', {'schedule': schedule} ))
