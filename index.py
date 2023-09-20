import json
from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

tasks = {}

with open('test.json') as f:
  tasks = json.load(f)

while True:
  print("Select difficult:")
  difficulty = input("(easy, medium, hard, exit) ")

  task_d = {}
  
  if difficulty == 'easy':
    task_d = tasks["easy"]
  elif difficulty == 'medium':
    task_d = tasks["medium"]
  elif difficulty == 'hard':
    task_d = tasks["hard"]
  else:
    break

  for key, task in task_d.items():
    print("Next task? (yes/no): ")
    next_task = input("")
    if next_task == 'no':
      break

    while True:
      print("\n" + task["question"])
      var = "\n".join(iter(input, ""))

      if1 = False
      if2 = False
      if3 = False

      try:
        exec(var)

        with Capturing() as output:
          exec(task["test1"]["ex"])
          exec(task["test2"]["ex"])
          exec(task["test3"]["ex"])

        print("out")
        print(output)
        
        if1 = eval(task["test1"]["if"])
        if2 = eval(task["test2"]["if"])
        if3 = eval(task["test3"]["if"])
      except:
        print("Error!")

      if if1 == True and if2 == True and if3 == True:
        print("Success")
        break
      else:
        print("Wrong")