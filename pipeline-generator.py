import os
import glob
import pipeline

changes = list(os.environ['CHANGES'].split(" "))
modules = {}

def getModules():
  for element in changes:
    if os.path.exists(element + '/isModule'):
      modules[element] = {}
      if os.path.exists(element + '/liquibase/changelog.xml'):
        modules[element]['liquibase'] = True
      if glob.glob(element + '/scripts/*.sql'):
        modules[element]['scripts'] = [os.path.basename(script) for script in glob.glob(element + '/scripts/*.sql')]
      if not modules[element]:
        modules.pop(element)
    continue
  if not modules:
    print("No changes in modules")
    exit(1)
  else:
    print(modules)

def generatePipeline():
  with open('generated-pipeline.yml', 'w') as f:
    f.write(pipeline.head())
    for module in modules:
      if 'liquibase' in modules[module]:
        f.write(pipeline.jobs_liquibase(module))
      if 'scripts' in modules[module]:
        for script in modules[module]['scripts']:
          f.write(pipeline.jobs_sql(module,script))
    f.close()

if __name__ == "__main__":
  getModules()
  generatePipeline()