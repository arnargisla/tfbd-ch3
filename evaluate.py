import fileinput
from ari import something

def main():
  counter = 0
  classes = {}
  for line in fileinput.input():
    class_name, observation_name = line.split()
    if class_name not in classes:
      classes[class_name] = set()
    classes[class_name].add(observation_name)

  for class_name in classes:
      print(class_name, classes[class_name])



if __name__ == "__main__":
  main()
