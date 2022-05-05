# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import errno
import yaml

from knack.log import get_logger
from knack.util import CLIError
from .vendored_sdks.pycomposefile import ComposeFile
from .vendored_sdks.azext_containerapp.custom import (
    create_containerapp, create_managed_environment)

logger = get_logger(__name__)


def create_containerapps_from_compose(cmd,
                                      resource_group_name,
                                      managed_env,
                                      compose_file_path='docker-compose.yml',
                                      transport=None,
                                      logs_workspace_name=None,
                                      location=None,
                                      tags=None):
    logger.info(   # pylint: disable=W1203
        f"Creating the Container Apps managed environment {managed_env} under {resource_group_name} in {location}.")

    managed_environment = create_managed_environment(cmd,
                                                     managed_env,
                                                     resource_group_name,
                                                     logs_workspace_name=logs_workspace_name,
                                                     tags=tags
                                                     )

    compose_yaml = load_yaml_file(compose_file_path)
    parsed_compose_file = ComposeFile(compose_yaml)

    containerapps_from_compose = []
    # Using the key to iterate to get the service name
    # pylint: disable=C0201,C0206
    for service_name in parsed_compose_file.ordered_services.keys():
        service = parsed_compose_file.services[service_name]
        logger.info(  # pylint: disable=W1203
            f"Creating the Container Apps instance for {service_name} under {resource_group_name} in {location}.")
        ingress_type, target_port = resolve_ingress_and_target_port(service)
        transport_setting = resolve_transport_from_cli_args(service_name, transport)
        startup_command, startup_args = resolve_service_startup_command(service)
        cpu, memory = validate_memory_and_cpu_setting(
            resolve_cpu_configuration_from_service(service),
            resolve_memory_configuration_from_service(service)
        )
        environment = resolve_environment_from_service(service)

        containerapps_from_compose.append(
            create_containerapp(cmd,
                                service_name,
                                resource_group_name,
                                image=service.image,
                                container_name=service.container_name,
                                managed_env=managed_environment["id"],
                                ingress=ingress_type,
                                target_port=target_port,
                                transport=transport_setting,
                                startup_command=startup_command,
                                args=startup_args,
                                cpu=cpu,
                                memory=memory,
                                env_vars=environment,
                                ))

    return containerapps_from_compose


def service_deploy_exists(service):
    return service.deploy is not None


def service_deploy_resources_exists(service):
    return service_deploy_exists(service) and service.deploy.resources is not None


def flatten_list(source_value):
    flat_list = []
    for sub_list in source_value:
        flat_list += sub_list
    return flat_list


def resolve_transport_from_cli_args(service_name, transport):
    if transport is not None:
        transport = flatten_list(transport)
        for setting in transport:
            key, value = setting.split('=')
            if key.lower() == service_name.lower():
                return value
    return 'auto'


def resolve_environment_from_service(service):
    env_array = []

    env_vars = service.resolve_environment_hierarchy()

    if env_vars is None:
        return None

    for k, v in env_vars.items():
        env_array.append(f"{k}={v}")

    return env_array


def valid_resource_settings():
    # vCPU and Memory reservations
    # https://docs.microsoft.com/azure/container-apps/containers#configuration
    return {
        "0.25": "0.5",
        "0.5": "1.0",
        "0.75": "1.5",
        "1.0": "2.0",
        "1.25": "2.5",
        "1.5": "3.0",
        "1.75": "3.5",
        "2.0": "4.0",
    }


def validate_memory_and_cpu_setting(cpu, memory):
    settings = valid_resource_settings()

    if cpu in settings.keys():  # pylint: disable=C0201
        if memory != settings[cpu]:
            if memory is not None:
                warning = f"Unsupported memory reservation request of {memory}."
                warning += f"The default value of {settings[cpu]}Gi will be used."
                logger.warning(warning)
            memory = settings[cpu]
        return (cpu, f"{memory}Gi")

    if cpu is not None:
        logger.warning(  # pylint: disable=W1203
            f"Invalid CPU reservation request of {cpu}. The default resource values will be used.")
    return (None, None)


def resolve_cpu_configuration_from_service(service):
    cpu = None
    if service_deploy_resources_exists(service):
        resources = service.deploy.resources
        if resources.reservations is not None and resources.reservations.cpus is not None:
            cpu = str(resources.reservations.cpus)
    elif service.cpus is not None:
        cpu = str(service.cpus)
    return cpu


def resolve_memory_configuration_from_service(service):
    memory = None
    if service_deploy_resources_exists(service):
        resources = service.deploy.resources
        if resources.reservations is not None and resources.reservations.memory is not None:
            memory = str(resources.reservations.memory.gigabytes())
    elif service.mem_reservation is not None:
        memory = str(service.mem_reservation.gigabytes())
    return memory


def resolve_ingress_and_target_port(service):
    # External Ingress Check
    if service.ports is not None:
        ingress_type = "external"
        target_port = int(service.ports[0].target)
    # Internal Ingress Check
    elif service.expose is not None:
        ingress_type = "internal"
        target_port = service.expose[0]
    else:
        ingress_type = None
        target_port = None
    return (ingress_type, target_port)


def resolve_service_startup_command(service):
    startup_command_array = []
    startup_args_array = []
    if service.entrypoint is not None:
        startup_command = service.entrypoint.command_string()
        startup_command_array.append(startup_command)
        if service.command is not None:
            startup_args = service.command.command_string()
            startup_args_array.append(startup_args)
    elif service.command is not None:
        startup_args = service.command.command_string()
        startup_command_array.append(startup_args)
        startup_args_array = None
    else:
        startup_command_array = None
        startup_args_array = None
    return (startup_command_array, startup_args_array)


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
