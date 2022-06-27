# GitLab pipeline generator for Oracle APEX applications

## Usage requirements
- Don't put space in directory or file names.
- Each module directory have to contain ```isModule``` file.
- Required directory structure for each module:
```
├───ModuleName
│   ├───scripts (.sql files)
│   └───liquibase (changelog.xml and related .sql files)
|   └───isModule
```

## How it works
- Current and previous commits get compared using ```git diff```.
- List of changed paths passed as list.
- Every path in list get checked. If directory contains ```isModule``` file, then it will be checked for existense of liquibase and sql files. If at least on of them exists, then module will be added as sub dictionary to ```modules``` dictionary and related elements will be added as keys. Example dictionary:
```
{'Module1': {'liquibase': True, 'scripts': ['f001.sql']}, 'Module2': {'scripts': ['f102.sql']}}
```
- Pipeline get generated with jobs for each module and elements and passed as artifact to next stage.

#### On branches other than master, only 'validate' stage will be executed.
