import random

teams = set()

while len(teams) < 500:
  class_name = random.choice(["CS", "ECE", "ECON", "FIN", "ACCY", "TEC", "ENG", "CHEM", "PSYC", "BIO", "AAS", "ACE", "ANSC"])
  num = random.randint(100, 500)
  purpose = random.choice(["homework group", "midterm study group", "final exam study group", "discussion group", "project group", "quiz study group"])
  name = "{}{} {}".format(class_name, num, purpose)

  if name not in teams:
    teams.add(name)

teams = list(teams)
for i in range(3000):
  user = random.randint(0, 1000)
  groupname = random.choice(teams)
  
  print("INSERT INTO GroupAssignment(AssignmentID, UserID, GroupName) VALUES ({}, {}, '{}');".format(i, user, groupname))

