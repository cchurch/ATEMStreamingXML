# PyTest
import pytest


def test_service_required(main, xml_compare):
    with xml_compare('default-84.xml', 'default-84.xml'):
        with pytest.raises(SystemExit):
            main()


def test_add_service(main, xml_compare, service_name):
    with xml_compare('default-84.xml', 'add-service.xml'):
        main('--service', service_name)


def test_add_service_no_change(main, xml_compare, service_name):
    with xml_compare('add-service.xml', 'add-service.xml'):
        main('-S', service_name)


def test_add_service_dry_run(main, xml_compare, service_name):
    with xml_compare('default-84.xml', 'default-84.xml'):
        main('--service', service_name, '--dry-run')


def test_remove_service(main, xml_compare, service_name):
    with xml_compare('add-service.xml', 'default-84.xml'):
        main('--service', service_name, '--remove-service')


def test_remove_service_no_change(main, xml_compare, service_name):
    with xml_compare('default-84.xml', 'default-84.xml'):
        main('-S', service_name, '--remove-service')


def test_remove_service_dry_run(main, xml_compare, service_name):
    with xml_compare('add-service.xml', 'add-service.xml'):
        main('--service', service_name, '--remove-service', '-n')
