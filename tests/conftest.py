# -*- coding: UTF-8 -*-

# Python
from __future__ import unicode_literals
import contextlib
import json
import os
import shutil

# Py.test
import pytest

# xmltodict
import xmltodict

# ATEMStreamingXML
try:
    import ATEMStreamingXML
except ImportError:
    from .. import ATEMStreamingXML


@pytest.fixture
def main():
    return ATEMStreamingXML.main


@pytest.fixture
def tmp_streaming_xml(tmp_path):
    tmp_file = os.path.join(str(tmp_path), 'Streaming.xml')
    os.environ['ATEM_STREAMING_XML'] = str(tmp_file)
    try:
        yield tmp_file
    finally:
        os.environ.pop('ATEM_STREAMING_XML')


@pytest.fixture
def xml_compare(tmp_streaming_xml):
    @contextlib.contextmanager
    def compare(before_xml, after_xml):
        before_file = os.path.join(os.path.dirname(__file__), before_xml)
        assert os.path.exists(before_file), before_file
        after_file = os.path.join(os.path.dirname(__file__), after_xml)
        assert os.path.exists(after_file), after_file
        shutil.copyfile(before_file, tmp_streaming_xml)
        try:
            yield tmp_streaming_xml
        finally:
            # Verify structure, not exact content.
            actual_data = xmltodict.parse(open(tmp_streaming_xml).read())
            actual_data = json.loads(json.dumps(actual_data, indent=4))
            expected_data = xmltodict.parse(open(after_file).read())
            expected_data = json.loads(json.dumps(expected_data, indent=4))
            assert actual_data == expected_data

    return compare


@pytest.fixture
def service_name():
    return 'Test Streaming Service'


@pytest.fixture
def server_name():
    return 'Primary'


@pytest.fixture
def server_url():
    return 'rtmp://primary.example.com/stream'


@pytest.fixture
def alt_server_name():
    return 'Bàckup'


@pytest.fixture
def alt_server_url():
    return 'rtmp://backup.example.com/stream'


@pytest.fixture
def profile_name():
    return 'Streaming High'


@pytest.fixture()
def alt_profile_name():
    return 'Streaming Low'


@pytest.fixture()
def config_resolution():
    return '1080p60'


@pytest.fixture()
def alt_config_resolution():
    return '1080p30'


@pytest.fixture()
def config_bitrate():
    return '9000000'


@pytest.fixture()
def alt_config_bitrate():
    return '6000000'


@pytest.fixture()
def config_audio_bitrate():
    return '128000'


@pytest.fixture()
def alt_config_audio_bitrate():
    return '192000'


@pytest.fixture()
def config_keyframe_interval():
    return '2'


@pytest.fixture()
def alt_config_keyframe_interval():
    return '3'
