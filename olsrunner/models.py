from django.db import models
from cassiopeia import riotapi
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, time

# Create your models here.

class Game(models.Model):
	team1 = models.IntegerField(default=0)
	team2 = models.IntegerField(default=0)
	winner = models.IntegerField(default=0)
	team1Player1 = models.IntegerField(default=0)
	team1Player2 = models.IntegerField(default=0)
	team1Player3 = models.IntegerField(default=0)
	team1Player4 = models.IntegerField(default=0)
	team1Player5 = models.IntegerField(default=0)
	team2Player1 = models.IntegerField(default=0)
	team2Player2 = models.IntegerField(default=0)
	team2Player3 = models.IntegerField(default=0)
	team2Player4 = models.IntegerField(default=0)
	team2Player5 = models.IntegerField(default=0)
	matchID = models.IntegerField(default=0)

	Number = models.IntegerField(default=0)
	filename = models.CharField(max_length=100)
	def __str__(self):
		team1name = Team.objects.get(teamID=self.team1).teamName
		team2name = Team.objects.get(teamID=self.team2).teamName
		gamename = team1name + ' Vs ' + team2name
		return gamename
	def team1name(self):
		return Team.objects.get(teamID=self.team1).teamName
	def team2name(self):
		return Team.objects.get(teamID=self.team2).teamName
class Team(models.Model):
	teamID = models.IntegerField(default=0)
	teamName = models.CharField(max_length=100)
	Captain = models.CharField(max_length=20)
	Player1 = models.CharField(max_length=20)
	Player2 = models.CharField(max_length=20)
	Player3 = models.CharField(max_length=20)
	Player4 = models.CharField(max_length=20)
	CaptainID = models.IntegerField(default=0)
	Player1ID = models.IntegerField(default=0)
	Player2ID = models.IntegerField(default=0)
	Player3ID = models.IntegerField(default=0)
	Player4ID = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	league = models.IntegerField(default=0)  # 0 = Demacia  1 = Noxus  2 = Piltover   3 = Zaun
	def __str__(self):
		return self.teamName

class Player(models.Model):
	SummonerNumber = models.IntegerField(default=0)
	PlayerIGN = models.CharField(max_length=30)
	PlayerName = models.CharField(max_length=50)
	IsCaptain = models.BooleanField(default=False)
	username = models.CharField(max_length=30, blank=True)
	

	def __str__(self):
		return self.PlayerIGN

class Stats(models.Model):
	PlayerID = models.IntegerField(default=0)
	Kills= models.IntegerField(default=0, blank=True)
	Deaths= models.IntegerField(default=0, blank=True)
	Assists= models.IntegerField(default=0, blank=True)
	GoldTotal= models.IntegerField(default=0, blank=True)
	GamesPlayed= models.IntegerField(default=0, blank=True)
	LargestCrit = models.IntegerField(default=0, blank=True)
	Creeps = models.IntegerField(default=0, blank=True)
	SecondsPlayed = models.IntegerField(default=0, blank=True)
	DamageDealt = models.IntegerField(default=0, blank=True)
	DamageReceived = models.IntegerField(default=0, blank=True)
	TeamKillTotal = models.IntegerField(default=0, blank=True)
	DoubleKills = models.IntegerField(default=0, blank=True)
	TripleKills = models.IntegerField(default=0, blank=True)
	QuadraKills = models.IntegerField(default=0, blank=True)
	PentaKills = models.IntegerField(default=0, blank=True) 
	def __str__(self):
		try:
			p =Player.objects.get(SummonerNumber=self.PlayerID)
			return p.PlayerIGN
		except ObjectDoesNotExist:
			riotapi.set_region("NA")
			s= riotapi.get_summoner_name(self.PlayerID)
			return s

class Week(models.Model):
	startdate= models.DateField(default=date.today)
	L0game1date= models.DateField(default=date.today, blank=True)
	L0game2date= models.DateField(default=date.today, blank=True)
	L0game3date= models.DateField(default=date.today, blank=True)
	L1game1date= models.DateField(default=date.today, blank=True)
	L1game2date= models.DateField(default=date.today, blank=True)
	L1game3date= models.DateField(default=date.today, blank=True)
	L2game1date= models.DateField(default=date.today, blank=True)
	L2game2date= models.DateField(default=date.today, blank=True)
	L2game3date= models.DateField(default=date.today, blank=True)
	L3game1date= models.DateField(default=date.today, blank=True)
	L3game2date= models.DateField(default=date.today, blank=True)
	L3game3date= models.DateField(default=date.today, blank=True)
	t = time(16, 20, 00)
	L0game1Time= models.TimeField(default=t, blank=True)
	L0game2Time= models.TimeField(default=t, blank=True)
	L0game3Time= models.TimeField(default=t, blank=True)
	L1game1Time= models.TimeField(default=t, blank=True)
	L1game2Time= models.TimeField(default=t, blank=True)
	L1game3Time= models.TimeField(default=t, blank=True)
	L2game1Time= models.TimeField(default=t, blank=True)
	L2game2Time= models.TimeField(default=t, blank=True)
	L2game3Time= models.TimeField(default=t, blank=True)
	L3game1Time= models.TimeField(default=t, blank=True)
	L3game2Time= models.TimeField(default=t, blank=True)
	L3game3Time= models.TimeField(default=t, blank=True)

	L0game1t1= models.IntegerField(default=0)
	L0game2t1= models.IntegerField(default=0)
	L0game3t1= models.IntegerField(default=0)
	L1game1t1= models.IntegerField(default=0)
	L1game2t1= models.IntegerField(default=0)
	L1game3t1= models.IntegerField(default=0)
	L2game1t1= models.IntegerField(default=0)
	L2game2t1= models.IntegerField(default=0)
	L2game3t1= models.IntegerField(default=0)
	L3game1t1= models.IntegerField(default=0)
	L3game2t1= models.IntegerField(default=0)
	L3game3t1= models.IntegerField(default=0)
	L0game1t2= models.IntegerField(default=0)
	L0game2t2= models.IntegerField(default=0)
	L0game3t2= models.IntegerField(default=0)
	L1game1t2= models.IntegerField(default=0)
	L1game2t2= models.IntegerField(default=0)
	L1game3t2= models.IntegerField(default=0)
	L2game1t2= models.IntegerField(default=0)
	L2game2t2= models.IntegerField(default=0)
	L2game3t2= models.IntegerField(default=0)
	L3game1t2= models.IntegerField(default=0)
	L3game2t2= models.IntegerField(default=0)
	L3game3t2= models.IntegerField(default=0)
	def __str__(self):
		return str(self.startdate)

class TourneyCode(models.Model):
	team1 = models.IntegerField(default=0)
	team2 = models.IntegerField(default=0)
	code = models.CharField(max_length=50)
	week = models.IntegerField(default=0)
	league = models.IntegerField(default=0)
	game = models.IntegerField(default=0)
	rift = models.IntegerField(default=0)
	def __str__(self):
		return "week: " + str(self.week) + " league: " + str(self.league) + "game: " + str(self.game) + "rift: " + str(self.rift) 
