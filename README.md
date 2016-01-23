# olsrunner
Runs the OLS website

##Requirements to run:

-Riot api key(must be set before most of the api calls)

-Riot tournament api key (must be set in certain instances)

-Python 3.5

-Django

-Must run the custom cassiopeia install in this repo

-django-tables2 https://github.com/bradleyayers/django-tables2

-Making all the migrations into a sqlite db

##How to:

-Clone the repo

-Install Python 3.5 and Django

-Install django-tables 2 from https://github.com/bradleyayers/django-tables2

-before all riotapi and baseriotapi calls make sure the api keys are set in both views.py and models.py

-install the custom cassiopeia install in cass/cassiopeia-master by running setup.py install
