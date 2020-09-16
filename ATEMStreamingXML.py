#!/usr/bin/env python

# Python
from __future__ import print_function, with_statement
import argparse
import difflib
import errno
import os
import sys
import xml.etree.ElementTree as ET

__version__ = '0.1.0'

ATEM_STREAMING_XML_DEFAULT = os.path.join('/Library', 'Application Support', 'Blackmagic Design', 'Switchers', 'Streaming.xml')
ATEM_STREAMING_XML = os.environ.get('ATEM_STREAMING_XML', ATEM_STREAMING_XML_DEFAULT)


def create_default_profiles(profiles_element):
    default_profiles = [
        dict(name='Streaming High', configs=[(60, 9000000), (30, 6000000)]),
        dict(name='Streaming Medium', configs=[(60, 7000000), (30, 4500000)]),
        dict(name='Streaming Low', configs=[(60, 4500000), (30, 3000000)]),
    ]
    for default_profile in default_profiles:
        profile_element = ET.SubElement(profiles_element, 'profile')
        name_element = ET.SubElement(profile_element, 'name')
        name_element.text = default_profile['name']
        for fps, bitrate in default_profile['configs']:
            config_element = ET.SubElement(profile_element, 'config')
            config_element.set('fps', '{}'.format(fps))
            config_element.set('resultion', '1080p')
            bitrate_element = ET.SubElement(config_element, 'bitrate')
            bitrate_element.text = '{}'.format(bitrate)
            keyframe_interval_element = ET.SubElement(config_element, 'keyframe-interval')
            keyframe_interval_element.text = '2'


def modify_service_element(service_element, **kwargs):
    server_name = kwargs.get('server_name', None)
    if not server_name:
        return
    server_url = kwargs.get('server_url', None)
    remove_server = kwargs.get('remove_server', False)
    servers_element = service_element.find('servers')
    if servers_element is None:
        servers_element = ET.SubElement(service_element, 'servers')
    server_element = None
    for _server_element in servers_element.findall('server'):
        _name_element = _server_element.find('name')
        if _name_element is not None and _name_element.text == server_name:
            server_element = _server_element
            break
    if remove_server:
        if server_element is not None:
            servers_element.remove(server_element)
        return
    if server_element is None:
        server_element = ET.SubElement(servers_element, 'server')
    name_element = server_element.find('name')
    if name_element is None:
        name_element = ET.SubElement(server_element, 'name')
    if name_element.text != server_name:
        name_element.text = server_name
    url_element = server_element.find('url')
    if url_element is None:
        url_element = ET.SubElement(server_element, 'url')
    if server_url and url_element.text != server_url:
        url_element.text = server_url


def modify_streaming_element(streaming_element, **kwargs):
    service_name = kwargs.get('service_name', None)
    remove_service = kwargs.get('remove_service', False)
    assert streaming_element.tag == 'streaming'
    service_element = None
    for _service_element in streaming_element.findall('service'):
        _name_element = _service_element.find('name')
        if _name_element is not None and _name_element.text == service_name:
            service_element = _service_element
            break
    if remove_service:
        if service_element is not None:
            streaming_element.remove(service_element)
        return
    if service_element is None:
        service_element = ET.SubElement(streaming_element, 'service')
        name_element = ET.SubElement(service_element, 'name')
        name_element.text = service_name
        servers_element = ET.SubElement(service_element, 'servers')
        profiles_element = ET.SubElement(service_element, 'profiles')
        create_default_profiles(profiles_element)
    modify_service_element(service_element, **kwargs)


def update_xml_indentation(element, text='\n\t', tail=''):
    if len(element):
        assert not (element.text or '').strip()  # Make sure there's no extra text except for whitespace.
        element.text = text
        element.tail = tail
        for n, child_element in enumerate(element):
            child_text = text + '\t'
            if n == (len(element) - 1):
                child_tail = text[:-1]
            elif tail:
                child_tail = text
            else:
                child_tail = '\n' + text
            update_xml_indentation(child_element, child_text, child_tail)
    else:
        element.tail = tail


def update_streaming_xml(**kwargs):
    parser = kwargs.get('parser', None)
    dry_run = kwargs.get('dry_run', False)
    tree = ET.parse(ATEM_STREAMING_XML)
    streaming_element = tree.getroot()
    original_xml = ET.tostring(streaming_element, encoding='UTF-8').decode('UTF-8')
    original_lines = original_xml.splitlines(True)

    modify_streaming_element(streaming_element, **kwargs)
    update_xml_indentation(streaming_element)

    modified_xml = ET.tostring(streaming_element, encoding='UTF-8').decode('UTF-8')
    modified_lines = modified_xml.splitlines(True)
    for line in difflib.context_diff(original_lines, modified_lines, fromfile='Streaming-old.xml', tofile='Streaming-new.xml'):
        print(line.rstrip('\n'))

    if not dry_run:
        try:
            tree.write(ATEM_STREAMING_XML, encoding='UTF-8', xml_declaration=True)
        except OSError as e:
            if e.errno == errno.EACCES:
                parser.exit(e.errno, '{}\nMaybe you need to run with sudo?'.format(e))
            else:
                parser.exit(e.errno, '{}'.format(e))


def main():
    parser = argparse.ArgumentParser(description='Modify ATEM Mini Pro Streaming.xml.')
    parser.add_argument(
        '-S',
        '--service',
        dest='service_name',
        metavar='SERVICE',
        required=True,
        help='Streaming service name',
    )
    parser.add_argument(
        '-N',
        '--server-name',
        dest='server_name',
        metavar='SERVER_NAME',
        help='Streaming server name',
    )
    parser.add_argument(
        '-U',
        '--server-url',
        dest='server_url',
        metavar='SERVER_URL',
        help='Streaming server RTMP URL',
    )
    parser.add_argument(
        '--remove',
        '--remove-service',
        dest='remove_service',
        action='store_true',
        default=False,
        help='Remove streaming service',
    )
    parser.add_argument(
        '--remove-server',
        dest='remove_server',
        action='store_true',
        default=False,
        help='Remove streaming server from a service',
    )
    parser.add_argument(
        '-n',
        '--dry-run',
        dest='dry_run',
        action='store_true',
        default=False,
        help='Show changes that would be made',
    )
    args = parser.parse_args()
    if args.server_name and not (args.server_url or args.remove_server):
        parser.error('The --server-name option requires either --server-url or --remove-server')
    kwargs = dict(vars(args), parser=parser)
    update_streaming_xml(**kwargs)


if __name__ == '__main__':
    main()
