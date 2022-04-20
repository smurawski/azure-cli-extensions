# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import unittest

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
        compose_file_name = f"{self._testMethodName}_compose.yml"
        docker_compose_file = open(compose_file_name, "w", encoding='utf-8')
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24),
            'workspace': self.create_random_name(prefix='containerapp-preview', length=24),
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        self.cmd(command_string, checks=[
            self.check('[].name', ['foo']),
            self.check('[] | length(@)', 1),
        ])

        if os.path.exists(compose_file_name):
            os.remove(compose_file_name)


class ContainerappComposePreviewIngressScenarioTest(ScenarioTest):
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_external_ingress(self, resource_group):
        compose_text = """
services:
  foo:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    ports: 8080:80
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        docker_compose_file = open(compose_file_name, "w", encoding='utf-8')
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24),
            'workspace': self.create_random_name(prefix='containerapp-preview', length=24),
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        self.cmd(command_string, checks=[
            self.check('[?name==`foo`].properties.configuration.ingress.targetPort', [80]),
            self.check('[?name==`foo`].properties.configuration.ingress.external', [True]),
        ])

        if os.path.exists(compose_file_name):
            os.remove(compose_file_name)


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
        compose_file_name = f"{self._testMethodName}_compose.yml"
        docker_compose_file = open(compose_file_name, "w", encoding='utf-8')
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24),
            'workspace': self.create_random_name(prefix='containerapp-preview', length=24),
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        self.cmd(command_string, checks=[
            self.check('[?name==`foo`].properties.configuration.ingress.targetPort', [3000]),
            self.check('[?name==`foo`].properties.configuration.ingress.external', [False]),
        ])

        if os.path.exists(compose_file_name):
            os.remove(compose_file_name)


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
        compose_file_name = f"{self._testMethodName}_compose.yml"
        docker_compose_file = open(compose_file_name, "w", encoding='utf-8')
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24),
            'workspace': self.create_random_name(prefix='containerapp-preview', length=24),
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        self.cmd(command_string, checks=[
            self.check('[?name==`foo`].properties.configuration.ingress.targetPort', [3000]),
            self.check('[?name==`foo`].properties.configuration.ingress.external', [True]),
        ])

        if os.path.exists(compose_file_name):
            os.remove(compose_file_name)


class ContainerappComposePreviewCommandScenarioTest(ScenarioTest):
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_with_command_string(self, resource_group):
        compose_text = """
services:
  foo:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    command: echo "hello world"
    expose:
      - "5000"
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        docker_compose_file = open(compose_file_name, "w", encoding='utf-8')
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24),
            'workspace': self.create_random_name(prefix='containerapp-preview', length=24),
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        self.cmd(command_string, checks=[
            self.check('[?name==`foo`].properties.template.containers[0].command[0]', "['echo \"hello world\"']"),
        ])

        if os.path.exists(compose_file_name):
            os.remove(compose_file_name)

    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_with_command_list(self, resource_group):
        compose_text = """
services:
  foo:
    image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
    command: ["echo", "hello world"]
    expose:
      - "5000"
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        docker_compose_file = open(compose_file_name, "w", encoding='utf-8')
        _ = docker_compose_file.write(compose_text)
        docker_compose_file.close()

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-preview', length=24),
            'workspace': self.create_random_name(prefix='containerapp-preview', length=24),
            'compose': compose_file_name,
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        self.cmd(command_string, checks=[
            self.check('[?name==`foo`].properties.template.containers[0].command[0]', "['echo \"hello world\"']"),
        ])

        if os.path.exists(compose_file_name):
            os.remove(compose_file_name)
