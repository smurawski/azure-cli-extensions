# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import errno
import yaml
from knack.log import get_logger
from knack.util import CLIError
from pycomposefile import ComposeFile
# pylint: disable=E0401
from azext_containerapp.custom import (
    create_containerapp, create_managed_environment)

logger = get_logger(__name__)


def create_containerapps_from_compose(cmd,
                                      resource_group_name,
                                      managed_env,
                                      compose_file_path='docker-compose.yml',
                                      location=None,
                                      tags=None):
    compose_yaml = load_yaml_file(compose_file_path)
    parsed_compose_file = ComposeFile(compose_yaml)

    logger.info(   # pylint: disable=W1203
        f"Creating the Container Apps managed environment {managed_env} under {resource_group_name} in {location}.")
    managed_environment = create_managed_environment(cmd,
                                                     managed_env,
                                                     resource_group_name,
                                                     tags=tags
                                                     )

    containerapps_from_compose = []
    # Using the key to iterate to get the service name
    # pylint: disable=C0201,C0206
    for service_name in parsed_compose_file.services.keys():
        service = parsed_compose_file.services[service_name]
        logger.info(  # pylint: disable=W1203
            f"Creating the Container Apps instance for {service_name} under {resource_group_name} in {location}.")
        containerapps_from_compose.append(
            create_containerapp(cmd,
                                service_name,
                                resource_group_name,
                                image=service.image,
                                managed_env=managed_environment["id"]
                                ))

    return containerapps_from_compose


def load_yaml_file(file_name):
    try:
        with open(file_name) as stream:  # pylint: disable=W1514
            return yaml.safe_load(stream)
    except (IOError, OSError) as ex:
        if getattr(ex, 'errno', 0) == errno.ENOENT:
            raise CLIError(f"{file_name} does not exist")  # pylint: disable=W0707
        raise
    except (yaml.parser.ParserError, UnicodeDecodeError) as ex:
        raise CLIError(f"Error parsing {file_name} ({str(ex)})")  # pylint: disable=W0707
