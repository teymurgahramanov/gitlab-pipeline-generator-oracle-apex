def head():
  head = """
stages:
  - validate
  - deploy
"""
  return head

def jobs_liquibase(module):
  jobs = f"""
validate-{module}-liquibase:
  stage: validate
  image: liquibase/liquibase:latest
  script:
    - liquibase --classpath={module}/liquibase --changeLogFile=changelog.xml --url=$DB_CLIENT@$DB_HOST --username=$DB_USER --password=$DB_PASS validate
  tags:
    - docker-shared

deploy-{module}-liquibase:
  stage: deploy
  image: liquibase/liquibase:latest
  script:
    - liquibase --classpath={module}/liquibase --changeLogFile=changelog.xml --url=$DB_CLIENT@$DB_HOST --username=$DB_USER --password=$DB_PASS --changelog-lock-wait-time-in-minutes=1 update
  tags:
    - docker-shared
  only:
    - master
"""
  return jobs

def jobs_sql(module,script):
  jobs = f"""
deploy-{module}-sql:
  stage: deploy
  image: oraclelinux:7-slim
  script:
    - yum install -y libaio
    - rpm -ivh https://download.oracle.com/otn_software/linux/instantclient/216000/oracle-instantclient-basic-21.6.0.0.0-1.x86_64.rpm
    - rpm -ivh https://download.oracle.com/otn_software/linux/instantclient/216000/oracle-instantclient-sqlplus-21.6.0.0.0-1.x86_64.rpm
    - exit | sqlplus -S $DB_USER/$DB_PASS@$DB_HOST @{module}/scripts/{script}
  tags:
    - docker-shared
  only:
    - master
"""
  return jobs