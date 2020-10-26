# PyTest
import pytest


def test_default_profiles(main, xml_compare, service_name):
    with xml_compare('empty.xml', 'default-profiles.xml'):
        main('--service', service_name, '--default-profiles')


def test_default_profiles_no_change(main, xml_compare, service_name):
    with xml_compare('default-profiles.xml', 'default-profiles.xml'):
        main('-S', service_name, '--default-profiles')


def test_add_profile(main, xml_compare, service_name, profile_name):
    with xml_compare('empty.xml', 'add-profile.xml'):
        main('--service', service_name, '--profile-name', profile_name)


def test_add_profile_no_change(main, xml_compare, service_name, profile_name):
    with xml_compare('add-profile.xml', 'add-profile.xml'):
        main('-S', service_name, '-P', profile_name)


def test_add_another_profile(main, xml_compare, service_name, alt_profile_name):
    with xml_compare('add-profile.xml', 'add-alt-profile.xml'):
        main('--service', service_name, '--profile-name', alt_profile_name)


def test_add_another_profile_no_change(main, xml_compare, service_name, alt_profile_name):
    with xml_compare('add-alt-profile.xml', 'add-alt-profile.xml'):
        main('-S', service_name, '-P', alt_profile_name)


def test_remove_profile_requires_profile_name(main, xml_compare, service_name):
    with xml_compare('add-alt-profile.xml', 'add-alt-profile.xml'):
        with pytest.raises(SystemExit):
            main('--service', service_name, '--remove-profile')


def test_remove_profile(main, xml_compare, service_name, alt_profile_name):
    with xml_compare('add-alt-profile.xml', 'add-profile.xml'):
        main('--service', service_name, '--profile-name', alt_profile_name, '--remove-profile')


def test_remove_profile_no_change(main, xml_compare, service_name, alt_profile_name):
    with xml_compare('add-profile.xml', 'add-profile.xml'):
        main('-S', service_name, '-P', alt_profile_name, '--remove-profile')
