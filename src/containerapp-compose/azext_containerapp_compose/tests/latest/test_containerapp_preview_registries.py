# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest  # pylint: disable=unused-import

from azure.cli.testsdk import (ResourceGroupPreparer)
from azure.cli.testsdk.decorators import serial_test
from azext_containerapp_compose.tests.latest.common import (ContainerappComposePreviewScenarioTest,  # pylint: disable=unused-import
                                                            write_test_file,
                                                            clean_up_test_file,
                                                            TEST_DIR)


class ContainerappComposePreviewRegistryAllArgsScenarioTest(ContainerappComposePreviewScenarioTest):
    @serial_test()
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_registry_all_args(self, resource_group):
        compose_text = """
services:
  foo:
    image: mcr.microsoft.com/azuredocs/containerapps-helloworld:latest
    ports: 8080:80
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        write_test_file(compose_file_name, compose_text)

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-compose', length=24),
            'workspace': self.create_random_name(prefix='containerapp-compose', length=24),
            'compose': compose_file_name,
            'registry_server': "foobar.azurecr.io",
            'registry_user': "foobar",
            'registry_pass': "snafu",
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        command_string += ' --registry-server {registry_server}'
        command_string += ' --registry-username {registry_user}'
        command_string += ' --registry-password {registry_pass}'

        self.cmd(command_string, checks=[
            self.check('[?name==`foo`].properties.configuration.registries[0].server', ["foobar.azurecr.io"]),
            self.check('[?name==`foo`].properties.configuration.registries[0].username', ["foobar"]),
            self.check('[?name==`foo`].properties.configuration.registries[0].passwordSecretRef', ["foobarazurecrio-foobar"]),  # pylint: disable=C0301
        ])

        clean_up_test_file(compose_file_name)


class ContainerappComposePreviewRegistryServerArgOnlyScenarioTest(ContainerappComposePreviewScenarioTest):
    @serial_test()
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_with_registry_server_arg_only(self, resource_group):
        compose_text = """
services:
  foo:
    image: mcr.microsoft.com/azuredocs/containerapps-helloworld:latest
    ports: 8080:80
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        write_test_file(compose_file_name, compose_text)

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-compose', length=24),
            'workspace': self.create_random_name(prefix='containerapp-compose', length=24),
            'compose': compose_file_name,
            'registry_server': "foobar.azurecr.io",
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        command_string += ' --registry-server {registry_server}'

        # This test fails because prompts are not supported in NoTTY environments
        self.cmd(command_string, expect_failure=True)

        clean_up_test_file(compose_file_name)
