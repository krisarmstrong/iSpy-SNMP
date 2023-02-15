"""
SNMP Interface Information Reader using Asyncio

This program is a multithreaded SNMP reader that retrieves interface information
via the SNMP interface MIB for all devices within a given subnet.

Author: Kris Armstrong
Date: [Date]
License: [License, if applicable]

PEP 8 Compliance:
- 4 spaces per indentation level
- Maximum line length of 79 characters
"""

import asyncio
from typing import List
from pysnmp.hlapi import (
    CommunityData, AsyncCommandGenerator,
    UdpTransportTarget, ContextData, ObjectIdentity,
    ObjectType, SnmpEngine, UsmUserData,
    BulkVarBinds, rfc1902
)
import ipaddress


async def read_interface_info(subnet: str, community: str) -> List[str]:
    """
    Read interface information via SNMP using the interface MIB for all devices
    within a given subnet.

    Args:
        subnet (str): The IP subnet to read interface information for.
        community (str): The SNMP community string to use for authentication.

    Returns:
        List[str]: A list of strings containing the interface information.
    """
    devices = get_devices_in_subnet(subnet)
    interface_info = []

    async with AsyncCommandGenerator() as ag:
        for device in devices:
            data = await get_interface_info(ag, device, community)
            interface_info.extend(data)

    return interface_info


def get_devices_in_subnet(subnet: str) -> List[str]:
    """
    Get a list of devices within a given subnet.

    Args:
        subnet (str): The IP subnet to get devices for.

    Returns:
        List[str]: A list of strings containing the IP addresses of devices
                   within the specified subnet.
    """
    ip_net = ipaddress.ip_network(subnet, strict=False)
    devices = [str(ip) for ip in ip_net.hosts()]
    return devices


async def get_interface_info(ag: AsyncCommandGenerator, device: str, community: str) -> List[str]:
    """
    Get interface information for a device via SNMP using the interface MIB.

    Args:
        ag (AsyncCommandGenerator): The AsyncCommandGenerator instance to use for the SNMP request.
        device (str): The IP address of the device to get interface information for.
        community (str): The SNMP community string to use for authentication.

    Returns:
        List[str]: A list of strings containing the interface information for the specified device.
    """
    transport_target = UdpTransportTarget((device, 161))
    community_data = CommunityData(community)

    oid = ObjectIdentity('IF-MIB', 'ifTable', 'ifEntry')
    error_indication, error_status, error_index, var_binds = await ag.bulkCmd(
        SnmpEngine(),
        community_data,
        transport_target,
        ContextData(),
        oid,
        maxCalls=50
    )

    if error_indication:
        raise Exception(f"SNMP error: {error_indication}")

    if error_status:
        raise Exception(f"SNMP error: {error_status}")

    interface_info = []

    for var_bind in var_binds:
        if_index = var_bind[0][-1]
        if_name = var_bind[1][1].prettyPrint()
        if_description = var_bind[2][1].prettyPrint()
        if_speed = var_bind[5][1].prettyPrint()

        interface_info.append(f"Interface {if_index}: {if_name} ({if_description}) at {if_speed} bps")

    return interface_info
