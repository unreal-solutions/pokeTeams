# pokeTeams

Basic Steps to use this script:

1) create a local version of pvpoke from his github
2) download python and pip modules
3) edit the roster.json file using the same conventions, to find the moves:
  a) go to pvpoke, team builder, add pokemon.
  b) click on the drop down, the top move is 0, and each move adds one
3) run teams.py, remember this takes time!  20 pokemon is over 700 different combinations, less goes faster, more goes slower
4) If you plan on running extremely large batches, you should consider using AWS free tier and terraform, you can spin 75 ec2 instances for 10 hours a month for free, and using lambda can make thousands of calls a minute
