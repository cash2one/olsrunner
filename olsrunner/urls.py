from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^archive/', include('archive.urls')),
	#url(r'^addgame/', views.addgames, name='Add Games to Official Record'),

	#administration pages
	url(r'^addplayers/', views.addPlayers, name="Form to add players"), #this is for adding a list of players to ols
	url(r'^addplayerlist/', views.addplayerlist, name="adding players"),
	url(r'^addTeam/', views.AddTeam, name="adding teams"),
	url(r'^updateIDs/', views.updateIDs, name="update player ids"),
	url(r'^updateTeams/', views.updateTeamIDs, name="update Team ids"),
	url(r'^addMatch/', views.addMatch, name="Add Match by ID"),
	url(r'^generatecodes/$', views.generatecodes,),
	url('^', include('django.contrib.auth.urls')),
	#url(r'^swipswap/$', views.swaprift1s,),

	#captain pages
	
	url(r'^reschedule/$', views.reschedule,),
	url(r'^codeused$', views.callback,),

	#player pages
	url(r'^standings/', views.standings, name="Current Split OLS Standings"),
	url(r'^m/([0-9]+)/$', views.match,),
	url(r'^stats/', views.overallstats, name="Current Split OLS statistics"),
	url(r'^p/(.*)/$', views.player_stats,),
	url(r'^t/(.*)/$', views.team_stats,),
	url(r'^schedule/$', views.schedule,),
]
