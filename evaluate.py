import fileinput
from adjusted_rand_index import rand_index

def main():
  counter = 0
  classes = {}
  for line in fileinput.input():
    class_name, observation_name, extension = [p for s in line.split(' ') for p in s.split('.')]
    if class_name not in classes:
      classes[class_name] = set()
    classes[class_name].add(observation_name)


  for class_name in classes:
      print(class_name, classes[class_name])
  
  clusters = list(classes.values())
  for cluster in clusters:
    pass #print(cluster)
  rand_index(clusters)



if __name__ == "__main__":
  main()
