# -*- coding: UTF-8 -*-

# Python
from __future__ import unicode_literals

# PyTest
import pytest


def test_service_required(main, xml_compare):
    with xml_compare('empty.xml', 'empty.xml'):
        with pytest.raises(SystemExit):
            main()


def test_add_service(main, xml_compare, service_name):
    with xml_compare('empty.xml', 'add-service.xml'):
        main('--service', service_name)


def test_add_service_no_change(main, xml_compare, service_name):
    with xml_compare('add-service.xml', 'add-service.xml'):
        main('-S', service_name)


def test_add_service_dry_run(main, xml_compare, service_name):
    with xml_compare('empty.xml', 'empty.xml'):
        main('--service', service_name, '--dry-run')


def test_remove_service(main, xml_compare, service_name):
    with xml_compare('add-service.xml', 'empty.xml'):
        main('--service', service_name, '--remove-service')


def test_remove_service_no_change(main, xml_compare, service_name):
    with xml_compare('empty.xml', 'empty.xml'):
        main('-S', service_name, '--remove-service')


def test_remove_service_dry_run(main, xml_compare, service_name):
    with xml_compare('add-service.xml', 'add-service.xml'):
        main('--service', service_name, '--remove-service', '-n')


def test_add_existing_service_no_change_84(main, xml_compare):
    with xml_compare('default-84.xml', 'default-84.xml'):
        main('-S', 'Facebook')


def test_add_existing_service_no_change_85(main, xml_compare):
    with xml_compare('default-85.xml', 'default-85.xml'):
        main('-S', 'Facebook')
