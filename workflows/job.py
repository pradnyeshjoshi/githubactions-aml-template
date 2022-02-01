# imports
from pathlib import Path
from azureml.core import Workspace
from azureml.core import ScriptRunConfig, Experiment, Environment
import os

subscription_id = os.getenv("SUBSCRIPTION_ID", default="<my-subscription-id>")
resource_group = os.getenv("RESOURCE_GROUP", default="<my-resource-group>")
workspace_name = os.getenv("WORKSPACE_NAME", default="<my-workspace-name>")
workspace_region = os.getenv("WORKSPACE_REGION", default="eastus2")

try:
    ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)
    # write the details of the workspace to a configuration file to the notebook library
    ws.write_config()
    print("Workspace configuration succeeded. Skip the workspace creation steps below")
except:
    print("Workspace not accessible. Change your parameters or create a new workspace below")

# # get workspace
# ws = Workspace.from_config()

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