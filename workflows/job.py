# imports
from pathlib import Path
from azureml.core import Workspace
from azureml.core import ScriptRunConfig, Experiment, Environment

# get workspace
ws = Workspace.from_config()

# get root of git repo
prefix = Path(__file__).parent

# test script
script_dir = str(prefix.joinpath("tests"))
script_name = "test.py"

# environment file
requirements_file = str(prefix.joinpath("requirements.txt"))

# azure ml settings
environment_name = "aml-test-environment"
experiment_name = "aml-test-experiment"
compute_name = "aml-cluster"

# create environment
env = Environment.from_pip_requirements(environment_name, requirements_file)

# create job config
src = ScriptRunConfig(
    source_directory=script_dir,
    script=script_name,
    environment=env,
    compute_target=compute_name,
)

# submit job
run = Experiment(ws, experiment_name).submit(src)
run.wait_for_completion(show_output=True)