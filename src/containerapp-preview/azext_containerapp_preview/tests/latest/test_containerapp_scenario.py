# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

from azure.cli.testsdk import (ScenarioTest, ResourceGroupPreparer)


TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


class ContainerappComposePreviewScenarioTest(ScenarioTest):

    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_no_existing_resources(self, resource_group):
        compose_text = """
services:
  foo:
    image: smurawski/printenv:latest
"""
        docker_compose_file = open("docker-compose.yml", "w")
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': 'test1'
        })

        self.cmd('containerapp compose create -g {rg} -e {environment}', checks=[
            self.check('[].name', ['foo']),
            self.check('[] | length(@)', 1)
        ])

        if os.path.exists("docker-compose.yml"):
            os.remove("docker-compose.yml")
