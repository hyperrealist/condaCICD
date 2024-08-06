import argparse
import os
import json


def main():
    parser = argparse.ArgumentParser(description='Parses Json and passes arguments to download-artifacts-sh')
    parser.add_argument("-o", "--organization", default="nsls2-conda-envs",
                        help="The organization the repository is under")
    parser.add_argument("-a", "--action_run", help="The ID of the workflow that was run", default="10189092932")
    parser.add_argument("-f", "--file_name", default="artifact_info",
                        help="jsonfile containg info about all artifacts created from some repository")
    parser.add_argument("-r", "--repository", default="nsls2-collection-tiled")
    parser.add_argument("-p", "--python_ver")
    args = parser.parse_args()
    artifact_command = f'''
    gh api \\
            -H \"Accept: application/vnd.github+json\" \\
            -H \"X-GitHub-Api-Version: 2022-11-28\" \\
            /repos/{args.organization}/{args.repository}/actions/artifacts >> {args.file_name}.json
    '''

    os.system(artifact_command)
    with open(f"{args.file_name}.json") as f:
        data = json.load(f)
        for element in data['artifacts']:
            if element['workflow_run'].get('id') == int(args.action_run) and os.path.splitext(element['name'])[1] != '.yml' and args.python_ver == element['name'].split('-')[2][2:]:
                os.system(f"echo \"link: {str(element['url'])}\"")
                os.system(f"GHA_TOKEN={os.environ['GHA_TOKEN']} bash download_artifacts_no_unzip.sh {args.repository} {args.organization} {str(element['id'])} {str(element['name'])}")

                print(args.repository)
                print(args.organization)
                print(str(element['id']))
                print(str(element['name']))

if __name__ == "__main__":
    main()