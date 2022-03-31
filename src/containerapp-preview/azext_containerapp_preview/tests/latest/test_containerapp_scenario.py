# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest

from azure.cli.testsdk import (ScenarioTest, ResourceGroupPreparer)


TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


@unittest.skip("Managed environment flaky")  # one test can only be run at one time, use this line to temporarily skip subsequent test
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
            'environment': self.create_random_name(prefix='containerapp-preview', length=24)
        })

        self.cmd('containerapp compose create --resource-group {rg} --environment {environment}', checks=[
            self.check('[].name', ['foo']),
            self.check('[] | length(@)', 1)
        ])

        if os.path.exists("docker-compose.yml"):
            os.remove("docker-compose.yml")


@unittest.skip("Managed environment flaky")  # one test can only be run at one time, use this line to temporarily skip subsequent test
class ContainerappComposePreviewIngressScenarioTest(ScenarioTest):
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_external_ingress(self, resource_group):
        compose_text = """
services:
  foo:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    ports: 8080:80
"""
        docker_compose_file = open("docker-compose.yml", "w")
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24)
        })

        self.cmd('containerapp compose create --resource-group {rg} --environment {environment} --compose-file-path docker-compose.yml', checks=[
            self.check('[].name', ['foo']),
            self.check('[] | length(@)', 1),
            self.check('[].properties.configuration.ingress.targetPort', [80]),
            self.check('[].properties.configuration.ingress.external', [True])
        ])

        if os.path.exists("docker-compose.yml"):
            os.remove("docker-compose.yml")


@unittest.skip("Managed environment flaky")  # one test can only be run at one time, use this line to temporarily skip subsequent test
class ContainerappComposePreviewIngressInternalScenarioTest(ScenarioTest):
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_internal_ingress(self, resource_group):
        compose_text = """
services:
  foo:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    expose:
      - "3000"
"""
        docker_compose_file = open("docker-compose.yml", "w")
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24)
        })

        self.cmd('containerapp compose create --resource-group {rg} --environment {environment} --compose-file-path docker-compose.yml', checks=[
            self.check('[].name', ['foo']),
            self.check('[] | length(@)', 1),
            self.check('[].properties.configuration.ingress.targetPort', [3000]),
            self.check('[].properties.configuration.ingress.external', [False])
        ])

        if os.path.exists("docker-compose.yml"):
            os.remove("docker-compose.yml")


# @unittest.skip("Managed environment flaky")  # one test can only be run at one time, use this line to temporarily skip subsequent test
class ContainerappComposePreviewIngressBothScenarioTest(ScenarioTest):
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_both_ingress(self, resource_group):
        compose_text = """
services:
  foo:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    ports: 4000:3000
    expose:
      - "5000"
"""
        docker_compose_file = open("docker-compose.yml", "w")
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24)
        })

        self.cmd('containerapp compose create --resource-group {rg} --environment {environment} --compose-file-path docker-compose.yml', checks=[
            self.check('[].name', ['foo']),
            self.check('[] | length(@)', 1),
            self.check('[].properties.configuration.ingress.targetPort', [3000]),
            self.check('[].properties.configuration.ingress.external', [True])
        ])

        if os.path.exists("docker-compose.yml"):
            os.remove("docker-compose.yml")
