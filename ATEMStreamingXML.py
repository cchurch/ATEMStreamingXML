#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Python
from __future__ import print_function, with_statement, unicode_literals
import argparse
import difflib
import errno
import os
import sys
import xml.etree.ElementTree as ET

__version__ = '0.1.4'


def get_streaming_xml_path():
    if sys.platform == 'darwin':
        default_path = os.path.join('/Library', 'Application Support', 'Blackmagic Design', 'Switchers', 'Streaming.xml')
    elif sys.platform == 'win32':  # pragma: no cover
        program_files_path = os.environ.get('ProgramFiles(x86)', os.environ.get('ProgramFiles'))
        default_path = os.path.join(program_files_path, 'Blackmagic Design', 'Blackmagic ATEM Switchers', 'ATEM Software Control', 'Streaming.xml')
    else:  # pragma: no cover
        default_path = 'Streaming.xml'
        if os.environ.get('ATEM_STREAMING_XML', None) is None:
            raise RuntimeError('unsupported platform: {}'.format(sys.platform))
    return os.environ.get('ATEM_STREAMING_XML', default_path)


def find_sub_element_by_name(parent_element, child_tag, name_text, name_tag='name'):
    for sub_element in parent_element.findall(child_tag):
        name_element = sub_element.find(name_tag)
        if name_element is not None and name_element.text == name_text:
            return sub_element


def create_or_update_sub_element(parent_element, child_tag, text=None):
    sub_element = parent_element.find(child_tag)
    if sub_element is None:
        sub_element = ET.SubElement(parent_element, child_tag)
    if text is not None:
        text = '{}'.format(text)
        if sub_element.text != text:
            sub_element.text = text
    return sub_element


def create_sub_element(parent_element, child_tag, name_text=None, name_tag='name'):
    sub_element = ET.SubElement(parent_element, child_tag)
    if name_text is not None:  # pragma: no cover
        create_or_update_sub_element(sub_element, name_tag, name_text)
    return sub_element


def get_or_create_config_element(profile_element, resolution, fps):
    for config_element in profile_element.findall('config'):
        if config_element.get('resolution') == resolution and config_element.get('fps') == fps:
            return config_element
        elif config_element.get('resultion') == resolution and config_element.get('fps') == fps:  # pragma: no cover
            config_element.attrib.pop('resultion')
            config_element.set('resolution', resolution)
            return config_element
    config_element = ET.SubElement(profile_element, 'config')
    config_element.set('resolution', resolution)
    config_element.set('fps', fps)
    return config_element


def update_profile_element(profile_element, **kwargs):
    profile_name = kwargs.get('profile_name')
    create_or_update_sub_element(profile_element, 'name', profile_name)
    profile_config = kwargs.get('profile_config')
    if not profile_config:
        return
    elif profile_config in ('1080p60', '1080p30'):
        resolution, fps = profile_config[:5], profile_config[-2:]
    else:  # pragma: no cover
        raise ValueError('invalid profile config: {}'.format(profile_config))
    config_element = get_or_create_config_element(profile_element, resolution, fps)
    if kwargs.get('remove_config', False):
        profile_element.remove(config_element)
        return profile_element
    bitrate = kwargs.get('bitrate')
    if bitrate is not None:
        if bitrate > 0:
            create_or_update_sub_element(config_element, 'bitrate', bitrate)
        else:
            bitrate_element = config_element.find('bitrate')
            if bitrate_element is not None:
                config_element.remove(bitrate_element)
    audio_bitrate = kwargs.get('audio_bitrate')
    if audio_bitrate is not None:
        if audio_bitrate > 0:
            create_or_update_sub_element(config_element, 'audio-bitrate', audio_bitrate)
        else:
            audio_bitrate_element = config_element.find('audio-bitrate')
            if audio_bitrate_element is not None:
                config_element.remove(audio_bitrate_element)
    keyframe_interval = kwargs.get('keyframe_interval')
    if keyframe_interval is not None:
        if keyframe_interval > 0:
            create_or_update_sub_element(config_element, 'keyframe-interval', keyframe_interval)
        else:
            keyframe_interval_element = config_element.find('keyframe-interval')
            if keyframe_interval_element is not None:
                config_element.remove(keyframe_interval_element)
    return profile_element


def update_server_element(server_element, **kwargs):
    create_or_update_sub_element(server_element, 'name', kwargs.get('server_name'))
    create_or_update_sub_element(server_element, 'url', kwargs.get('server_url'))
    return server_element


def update_service_element(service_element, **kwargs):
    servers_element = create_or_update_sub_element(service_element, 'servers')
    server_name = kwargs.get('server_name')
    if server_name:
        server_element = find_sub_element_by_name(servers_element, 'server', server_name)
        if kwargs.get('remove_server', False):
            if server_element is not None:
                servers_element.remove(server_element)
        else:
            if server_element is None:
                server_element = create_sub_element(servers_element, 'server', server_name)
            update_server_element(server_element, **kwargs)
    profiles_element = create_or_update_sub_element(service_element, 'profiles')
    if kwargs.get('default_profiles', False):
        profiles_list = [
            dict(profile_name='Streaming High', profile_config='1080p60', bitrate=9000000),
            dict(profile_name='Streaming High', profile_config='1080p30', bitrate=6000000),
            dict(profile_name='Streaming Medium', profile_config='1080p60', bitrate=7000000),
            dict(profile_name='Streaming Medium', profile_config='1080p30', bitrate=4500000),
            dict(profile_name='Streaming Low', profile_config='1080p60', bitrate=4500000),
            dict(profile_name='Streaming Low', profile_config='1080p30', bitrate=3000000),
        ]
        for profile_kwargs in profiles_list:
            profile_kwargs.setdefault('audio_bitrate', 128000)
            profile_kwargs.setdefault('keyframe_interval', 2)
    elif kwargs.get('profile_name'):
        profiles_list = [kwargs]
    else:
        profiles_list = []
    for profile_kwargs in profiles_list:
        profile_name = profile_kwargs.get('profile_name')
        profile_element = find_sub_element_by_name(profiles_element, 'profile', profile_name)
        if kwargs.get('remove_profile', False):
            if profile_element is not None:
                profiles_element.remove(profile_element)
        else:
            if profile_element is None:
                profile_element = create_sub_element(profiles_element, 'profile', profile_name)
            update_profile_element(profile_element, **profile_kwargs)
    return service_element


def update_streaming_element(streaming_element, **kwargs):
    assert streaming_element.tag == 'streaming'
    service_name = kwargs.get('service_name')
    service_element = find_sub_element_by_name(streaming_element, 'service', service_name)
    if kwargs.get('remove_service', False):
        if service_element is not None:
            streaming_element.remove(service_element)
    else:
        if service_element is None:
            service_element = create_sub_element(streaming_element, 'service', service_name)
        update_service_element(service_element, **kwargs)


def update_xml_indentation(element, text='\n\t', tail=''):
    if len(element):
        assert not (element.text or '').strip()  # Make sure there's no extra text except for whitespace.
        element.text = text
        element.tail = (element.tail or '').rstrip() + tail
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
        element.tail = (element.tail or '').rstrip() + tail


def element_tostring(element, encoding=None, method=None):
    class dummy:
        pass

    data = []
    file = dummy()
    file.write = data.append
    ET.ElementTree(element).write(file, encoding, method=method)
    if sys.version_info[0] == 2:  # pragma: no cover
        data = [d.encode('UTF-8') if isinstance(d, unicode) else d for d in data[:]]  # noqa
        return str('').join(data)
    else:
        return b''.join(data)


def update_streaming_xml(**kwargs):
    parser = kwargs.get('parser', None)
    dry_run = kwargs.get('dry_run', False)
    xml_parser = ET.XMLParser(encoding='UTF-8')
    tree = ET.parse(get_streaming_xml_path(), parser=xml_parser)
    streaming_element = tree.getroot()
    original_xml = element_tostring(streaming_element, encoding='UTF-8').decode('UTF-8')
    original_lines = original_xml.splitlines(True)

    update_streaming_element(streaming_element, **kwargs)
    update_xml_indentation(streaming_element)

    updated_xml = element_tostring(streaming_element, encoding='UTF-8').decode('UTF-8')
    updated_lines = updated_xml.splitlines(True)
    for line in difflib.context_diff(original_lines, updated_lines, fromfile='Streaming-old.xml', tofile='Streaming-new.xml'):
        print(line.rstrip('\n'))

    if not dry_run:
        try:
            tree.write(get_streaming_xml_path(), encoding='UTF-8', xml_declaration=True)
        except (IOError, OSError) as e:  # pragma: no cover
            if e.errno == errno.EACCES:
                if sys.platform == 'win32':
                    parser.exit(e.errno, '{}\nTry running the command as an Administrator.'.format(e))
                else:
                    parser.exit(e.errno, '{}\nTry running the command with sudo.'.format(e))
            else:
                parser.exit(e.errno, '{}'.format(e))


def main(*args):
    parser = argparse.ArgumentParser(
        description='Modify ATEM Mini Pro Streaming.xml.',
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
    )
    parser.add_argument(
        '-S',
        '--service',
        dest='service_name',
        metavar='SERVICE',
        required=True,
        help='Streaming service name to update/remove',
    )
    parser.add_argument(
        '-N',
        '--server-name',
        dest='server_name',
        metavar='SERVER_NAME',
        help='Streaming server name to update/remove',
    )
    parser.add_argument(
        '-U',
        '--server-url',
        dest='server_url',
        metavar='SERVER_URL',
        help='Streaming server RTMP URL',
    )
    parser.add_argument(
        '--default-profiles',
        dest='default_profiles',
        action='store_true',
        default=False,
        help='Create or update default profiles for a streaming service',
    )
    parser.add_argument(
        '-P',
        '--profile-name',
        dest='profile_name',
        metavar='PROFILE_NAME',
        help='Streaming profile name to update/remove',
    )
    parser.add_argument(
        '-C',
        '--profile-config',
        dest='profile_config',
        choices=['1080p60', '1080p30'],
        help='Streaming profile config resolution and frame rate to update/remove',
    )
    parser.add_argument(
        '--br',
        '--bitrate',
        dest='bitrate',
        type=int,
        help='Streaming profile config bitrate',
    )
    parser.add_argument(
        '--abr',
        '--audio-bitrate',
        dest='audio_bitrate',
        type=int,
        help='Streaming profile config audio bitrate',
    )
    parser.add_argument(
        '--ki',
        '--keyframe-interval',
        dest='keyframe_interval',
        type=int,
        help='Streaming profile config keyframe interval',
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
        '--remove-profile',
        dest='remove_profile',
        action='store_true',
        default=False,
        help='Remove streaming profile from a service',
    )
    parser.add_argument(
        '--remove-config',
        dest='remove_config',
        action='store_true',
        default=False,
        help='Remove streaming profile config from a profile',
    )
    parser.add_argument(
        '-n',
        '--dry-run',
        dest='dry_run',
        action='store_true',
        default=False,
        help='Show changes that would be made',
    )
    ns = parser.parse_args(args or None)
    if ns.server_name and not (ns.server_url or ns.remove_server):
        parser.error('The --server-name option requires either --server-url or --remove-server')
    if ns.remove_server and not ns.server_name:
        parser.error('The --remove-server option requires --server-name')
    if ns.remove_profile and not ns.profile_name:
        parser.error('The --remove-profile option requires --profile-name')
    if ns.profile_config and not ns.profile_name:
        parser.error('The --profile-config option requires --profile-name')
    if ns.remove_config and not ns.profile_config:
        parser.error('The --remove-config option requires --profile-config')

    kwargs = dict(vars(ns), parser=parser)
    update_streaming_xml(**kwargs)


if __name__ == '__main__':
    main()
