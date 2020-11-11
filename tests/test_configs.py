# -*- coding: UTF-8 -*-

# Python
from __future__ import unicode_literals

# PyTest
import pytest


def test_invalid_config(main, xml_compare, service_name, profile_name,):
    with xml_compare('empty.xml', 'empty.xml'):
        with pytest.raises(SystemExit):
            main('-S', service_name, '-P', profile_name, '-C', '1080i60')


def test_config_requires_profile_name(main, xml_compare, service_name, config_resolution):
    with xml_compare('add-alt-config.xml', 'add-alt-config.xml'):
        with pytest.raises(SystemExit):
            main('--service', service_name, '--profile-config', config_resolution, '--remove-config')


def test_add_config(main, xml_compare, service_name, profile_name, config_resolution):
    with xml_compare('empty.xml', 'add-config.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution)


def test_add_config_no_change(main, xml_compare, service_name, profile_name, config_resolution):
    with xml_compare('add-config.xml', 'add-config.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution)


def test_add_another_config(main, xml_compare, service_name, profile_name, alt_config_resolution):
    with xml_compare('add-config.xml', 'add-alt-config.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', alt_config_resolution)


def test_add_another_config_no_change(main, xml_compare, service_name, profile_name, alt_config_resolution):
    with xml_compare('add-alt-config.xml', 'add-alt-config.xml'):
        main('-S', service_name, '-P', profile_name, '-C', alt_config_resolution)


def test_add_config_bitrate(main, xml_compare, service_name, profile_name, config_resolution, config_bitrate):
    with xml_compare('empty.xml', 'add-config-bitrate.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--bitrate', config_bitrate)


def test_add_config_bitrate_no_change(main, xml_compare, service_name, profile_name, config_resolution, config_bitrate):
    with xml_compare('add-config-bitrate.xml', 'add-config-bitrate.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--br', config_bitrate)


def test_update_config_bitrate(main, xml_compare, service_name, profile_name, config_resolution, alt_config_bitrate):
    with xml_compare('add-config-bitrate.xml', 'update-config-bitrate.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--bitrate', alt_config_bitrate)


def test_update_config_bitrate_no_change(main, xml_compare, service_name, profile_name, config_resolution, alt_config_bitrate):
    with xml_compare('update-config-bitrate.xml', 'update-config-bitrate.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--br', alt_config_bitrate)


def test_remove_config_bitrate(main, xml_compare, service_name, profile_name, config_resolution):
    with xml_compare('add-config-bitrate.xml', 'add-config.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--bitrate', '0')


def test_remove_config_bitrate_no_change(main, xml_compare, service_name, profile_name, config_resolution):
    with xml_compare('add-config.xml', 'add-config.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--br', '-1')


def test_add_config_audio_bitrate(main, xml_compare, service_name, profile_name, config_resolution, config_audio_bitrate):
    with xml_compare('empty.xml', 'add-config-audio-bitrate.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--audio-bitrate', config_audio_bitrate)


def test_add_config_audio_bitrate_no_change(main, xml_compare, service_name, profile_name, config_resolution, config_audio_bitrate):
    with xml_compare('add-config-audio-bitrate.xml', 'add-config-audio-bitrate.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--abr', config_audio_bitrate)


def test_update_config_audio_bitrate(main, xml_compare, service_name, profile_name, config_resolution, alt_config_audio_bitrate):
    with xml_compare('add-config-audio-bitrate.xml', 'update-config-audio-bitrate.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--audio-bitrate', alt_config_audio_bitrate)


def test_update_config_audio_bitrate_no_change(main, xml_compare, service_name, profile_name, config_resolution, alt_config_audio_bitrate):
    with xml_compare('update-config-audio-bitrate.xml', 'update-config-audio-bitrate.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--abr', alt_config_audio_bitrate)


def test_remove_config_audio_bitrate(main, xml_compare, service_name, profile_name, config_resolution):
    with xml_compare('add-config-audio-bitrate.xml', 'add-config.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--audio-bitrate', '0')


def test_remove_config_audio_bitrate_no_change(main, xml_compare, service_name, profile_name, config_resolution):
    with xml_compare('add-config.xml', 'add-config.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--abr', '-1')


def test_add_config_keyframe_interval(main, xml_compare, service_name, profile_name, config_resolution, config_keyframe_interval):
    with xml_compare('empty.xml', 'add-config-keyframe-interval.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--keyframe-interval', config_keyframe_interval)


def test_add_config_keyframe_interval_no_change(main, xml_compare, service_name, profile_name, config_resolution, config_keyframe_interval):
    with xml_compare('add-config-keyframe-interval.xml', 'add-config-keyframe-interval.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--ki', config_keyframe_interval)


def test_update_config_keyframe_interval(main, xml_compare, service_name, profile_name, config_resolution, alt_config_keyframe_interval):
    with xml_compare('add-config-keyframe-interval.xml', 'update-config-keyframe-interval.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--keyframe-interval', alt_config_keyframe_interval)


def test_update_config_keyframe_interval_no_change(main, xml_compare, service_name, profile_name, config_resolution, alt_config_keyframe_interval):
    with xml_compare('update-config-keyframe-interval.xml', 'update-config-keyframe-interval.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--ki', alt_config_keyframe_interval)


def test_remove_config_keyframe_interval(main, xml_compare, service_name, profile_name, config_resolution):
    with xml_compare('add-config-keyframe-interval.xml', 'add-config.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', config_resolution, '--keyframe-interval', '0')


def test_remove_config_keyframe_interval_no_change(main, xml_compare, service_name, profile_name, config_resolution):
    with xml_compare('add-config.xml', 'add-config.xml'):
        main('-S', service_name, '-P', profile_name, '-C', config_resolution, '--ki', '-1')


def test_remove_config_requires_config_resolution(main, xml_compare, service_name, profile_name):
    with xml_compare('add-alt-config.xml', 'add-alt-config.xml'):
        with pytest.raises(SystemExit):
            main('--service', service_name, '--profile-name', profile_name, '--remove-config')


def test_remove_config(main, xml_compare, service_name, profile_name, alt_config_resolution):
    with xml_compare('add-alt-config.xml', 'remove-config.xml'):
        main('--service', service_name, '--profile-name', profile_name, '--profile-config', alt_config_resolution, '--remove-config')


def test_remove_config_no_change(main, xml_compare, service_name, profile_name, alt_config_resolution):
    with xml_compare('remove-config.xml', 'remove-config.xml'):
        main('-S', service_name, '-P', profile_name, '-C', alt_config_resolution, '--remove-config')
