# PyTest
import pytest


def test_server_name_requires_remove_or_url(main, xml_compare, service_name, server_name):
    with xml_compare('default-84.xml', 'default-84.xml'):
        with pytest.raises(SystemExit):
            main('--service', service_name, '--server-name', server_name)


def test_add_server(main, xml_compare, service_name, server_name, server_url):
    with xml_compare('default-84.xml', 'add-server.xml'):
        main('--service', service_name, '--server-name', server_name, '--server-url', server_url)


def test_add_server_no_change(main, xml_compare, service_name, server_name, server_url):
    with xml_compare('add-server.xml', 'add-server.xml'):
        main('-S', service_name, '-N', server_name, '-U', server_url)


def test_add_another_server(main, xml_compare, service_name, alt_server_name, alt_server_url):
    with xml_compare('add-server.xml', 'add-alt-server.xml'):
        main('--service', service_name, '--server-name', alt_server_name, '--server-url', alt_server_url)


def test_add_another_server_no_change(main, xml_compare, service_name, alt_server_name, alt_server_url):
    with xml_compare('add-alt-server.xml', 'add-alt-server.xml'):
        main('-S', service_name, '-N', alt_server_name, '-U', alt_server_url)


def test_update_server_url(main, xml_compare, service_name, server_name, alt_server_url):
    with xml_compare('add-server.xml', 'update-server.xml'):
        main('--service', service_name, '--server-name', server_name, '--server-url', alt_server_url)


def test_update_server_url_no_change(main, xml_compare, service_name, server_name, alt_server_url):
    with xml_compare('update-server.xml', 'update-server.xml'):
        main('-S', service_name, '-N', server_name, '-U', alt_server_url)


def test_remove_server_requires_server_name(main, xml_compare, service_name):
    with xml_compare('add-alt-server.xml', 'add-alt-server.xml'):
        with pytest.raises(SystemExit):
            main('--service', service_name, '--remove-server')


def test_remove_server(main, xml_compare, service_name, alt_server_name):
    with xml_compare('add-alt-server.xml', 'add-server.xml'):
        main('--service', service_name, '--server-name', alt_server_name, '--remove-server')


def test_remove_server_no_change(main, xml_compare, service_name, alt_server_name):
    with xml_compare('add-server.xml', 'add-server.xml'):
        main('-S', service_name, '-N', alt_server_name, '--remove-server')
