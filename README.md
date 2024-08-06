# testing_conda_artifact_scenarios

### Requirements for using the test-conda-environment action:
- You must somehow get the conda environment as an artifact in the workflow run before action use

### Workflow files:
**Examples of how Conda Environments are gotten as an artifact in the workflow run**

- Scenario 1: Conda Environment is built from earlier job from the same workflow
- Scenario 2: Conda Environment from a different repository on GitHub
- Scenario 3: Conda environment is taken from Zenodo

## Current Repo Files Explanation 

### configs
Information contained within each config file is used as metadata when being uploaded to Zenodo.
Another big use case is the env_name key being used as the CONDA_PACKED_NAME inside each workflow.

Limitations:
- Every time you want to test a different Conda Environment, the keys version and env_name should be changed

### envs
Used inside Scenario 1 to build a conda environment using the step which utilizes the umamba action

### download_from_github
Used in the second scenario and is a slight modification of the parse_for_artifacts script that downloads artifacts of 
a specific python version to avoid running out of memory for the runner. Then these same artifacts are uploaded to the
 current GitHub workflow run.

Notes:
- Unlike the other two scenarios, the unzipped files after downloads have to be moved to the artifacts folder. I could 
have a modified download-artifacts.sh file that doesn't unzip the files and upload the artifact in it's zipped format
however because the yml file is also uploaded, unzipping the files are necessary

### download_from_zenodo
Used in the third scenario and takes the files contained inside a Zenodo record only with a specific python version.
The script handles putting the files inside artifacts directory so no worries there. Then this artifacts directory is 
uploaded as an artifact

## Action Files Explanation

### supervisor
Contains information of simulated PV's that is on the BlackHole IOC

### beamline_status_to_md
Goes through jobs for a specific python version and generates a markdown table containing information on
the testing results for each beamline as well as debugging messages. A markdown table is created in the process
where it is copied into the GitHub Summary context in the actual workflow file

Limitations:
- In order to parse for the Beamline name (ex. csx) the name of the actual job for tesing-conda-environment should 
follow the existing format. Also when accessing this name from the GitHub REST API, because these are nested jobs
it requires more parsing. Just keep in mind changing the naming convention to not break parsing

### parse_for_artifacts

takes in a workflow run id most importantly and downloads all artifacts under that run id. Should only download the
artifacts containing the conda environment tar file

### specifal_config
Should be the script that attempts to solve compatibility issues between the conda environment and the 
Ipython startup files. This is the direct file that affects the results shown in the Github Summary table

### upload_artifacts
Isn't actually used in current repo, take a look at StaticYolt/nsls2-collection-tiled for use case. Contains
python code that interacts to zenodo api to create a new version draft containing the conda environments artifacts from
the current workflow run. 

Limitations:
- Doesn't work if there is a pre-existing new version draft. You would need to delete the draft for this script to work.

### upload_on_success
Figures out the success rate of tests across beamlines from all python version which is used to 
determine whether to use upload_artifact methods to create that new version draft on Zenodo.

## Additional Notes
For each scenario, switching between them requires different things

In scenario one, it requires the packed name of the files in configs and envs to be the same as the version you want

In scenario two and three, it should only require the configs name to be the version you want