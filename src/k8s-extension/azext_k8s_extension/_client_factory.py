# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.profiles import ResourceType
from . import consts


def cf_k8s_extension(cli_ctx, **kwargs):
    from .vendored_sdks import SourceControlConfigurationClient
    return get_mgmt_service_client(cli_ctx, SourceControlConfigurationClient, **kwargs)


def cf_k8s_extension_operation(cli_ctx, _):
    return cf_k8s_extension(cli_ctx).extensions


def cf_k8s_cluster_extension_types_operation(cli_ctx, _):
    return cf_k8s_extension(cli_ctx, consts.EXTENSION_TYPE_API_VERSION).cluster_extension_types


def cf_k8s_cluster_extension_type_operation(cli_ctx, _):
    return cf_k8s_extension(cli_ctx, consts.EXTENSION_TYPE_API_VERSION).cluster_extension_type


def cf_k8s_location_extension_types_operation(cli_ctx, _):
    return cf_k8s_extension(cli_ctx, consts.EXTENSION_TYPE_API_VERSION).location_extension_types


def cf_k8s_extension_type_versions_operation(cli_ctx, _):
    return cf_k8s_extension(cli_ctx, consts.EXTENSION_TYPE_API_VERSION).extension_type_versions


def cf_resource_groups(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id).resource_groups


def cf_resources(cli_ctx, subscription_id=None):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id).resources


def cf_log_analytics(cli_ctx, subscription_id=None):
    from azure.mgmt.loganalytics import LogAnalyticsManagementClient  # pylint: disable=no-name-in-module
    return get_mgmt_service_client(cli_ctx, LogAnalyticsManagementClient, subscription_id=subscription_id)


def _resource_providers_client(cli_ctx):
    from azure.mgmt.resource import ResourceManagementClient
    return get_mgmt_service_client(cli_ctx, ResourceManagementClient).providers
