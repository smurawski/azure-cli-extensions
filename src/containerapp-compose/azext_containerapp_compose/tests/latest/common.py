# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
from azure.cli.testsdk import (ScenarioTest)

TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


def write_test_file(filename, content):
    test_file = open(filename, "w", encoding='utf-8')
    _ = test_file.write(content)
    test_file.close()


def clean_up_test_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


class ContainerappComposePreviewScenarioTest(ScenarioTest):
    def __init__(self,
                 method_name,
                 config_file=None,
                 recording_name=None,
                 recording_processors=None,
                 replay_processors=None,
                 recording_patches=None,
                 replay_patches=None):
        super().__init__(method_name,
                         config_file,
                         recording_name,
                         recording_processors,
                         replay_processors,
                         recording_patches,
                         replay_patches)
        self.cmd("az extension add --name containerapp")
