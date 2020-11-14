# -*- coding: UTF-8 -*-

# Python
from __future__ import unicode_literals

# PyTest
import pytest


def test_display_help(main, xml_compare, capsys):
    with xml_compare('empty.xml', 'empty.xml'):
        with pytest.raises(SystemExit):
            main('--help')
        out, err = capsys.readouterr()
        assert 'usage:' in out


def test_display_version(main, xml_compare, capsys, version):
    with xml_compare('empty.xml', 'empty.xml'):
        with pytest.raises(SystemExit):
            main('--version')
        out, err = capsys.readouterr()
        assert version in out or version in err
