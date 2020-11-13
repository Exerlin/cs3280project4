#!/usr/bin/env python3
'''
Script that contains code to verify the validity of IP and subnet addresses.
Can also get the subnet given an IP address.
'''

import re

def verify_ip_address_format(the_address):
    '''
    verify_ip_address_format(the_address) that returns a boolean
    Returns True if the given address is in the format of an ip address.
    Returns False otherwise.
    '''
    regex_string_ip_address = re.compile(r'^[0-9]{3}[.]{1}([0-9]{1,3}[.]{1}){2}[0-9]{1,3}$')

    if regex_string_ip_address.search(the_address) is None:
        return False
    return True

def is_subnet_mask_in_bit_format(the_subnet_mask):
    '''
    is_subnet_mask_in_bit_format(the_subnet_mask) that returns a boolean
    Returns True if the subnet mask is in bit form.
    Returns False otherwise.
    '''
    regex_string_subnet_mask_bit_format = re.compile(r'^([0-2]?[0-9]|30|31)$')
    if regex_string_subnet_mask_bit_format.search(the_subnet_mask) is None:
        return False
    return True

def verify_subnet_mask_format(the_subnet_mask):
    '''
    verify_subnet_mask_format(the_subnet_mask) that returns a boolean
    Returns True if the given subnet mask is in the format of a subnet mask.
    Returns False otherwise.
    '''
    if is_subnet_mask_in_bit_format(the_subnet_mask):
        return True
    regex_string_subnet_mask_address_format = re.compile(r'^(((128|192|224|240|248|252|254|255|0(?=\.0))\.){3}(128|192|224|240|248|252|254|0))$')
    if regex_string_subnet_mask_address_format.search(the_subnet_mask) is None:
        return False
    divided_subnet_mask = the_subnet_mask.split(".")
    if divided_subnet_mask[0] < divided_subnet_mask[1]:
        return False
    if divided_subnet_mask[1] < divided_subnet_mask[2]:
        return False
    if divided_subnet_mask[2] < divided_subnet_mask[3]:
        return False
    return True

def get_full_subnet_mask(number_of_bits):
    '''
    get_full_subnet_mask(number_of_bits) that returns a string
    Returns a formatted subnet mask given a number of bits.
    Returns False if number of bits given is invalid.
    '''
    number_of_bits = int(number_of_bits)
    if number_of_bits > 31 or number_of_bits < 0:
        return False
    full_subnet_mask = ""
    for current_division in range(4):
        if full_subnet_mask != "":
            full_subnet_mask += "."

        if number_of_bits > 7:
            full_subnet_mask += "255"
            number_of_bits -= 8
        elif number_of_bits == 7:
            full_subnet_mask += "254"
            number_of_bits -= 7
        elif number_of_bits == 6:
            full_subnet_mask += "252"
            number_of_bits -= 6
        elif number_of_bits == 5:
            full_subnet_mask += "248"
            number_of_bits -= 5
        elif number_of_bits == 4:
            full_subnet_mask += "240"
            number_of_bits -= 4
        elif number_of_bits == 3:
            full_subnet_mask += "224"
            number_of_bits -= 3
        elif number_of_bits == 2:
            full_subnet_mask += "192"
            number_of_bits -= 2
        elif number_of_bits == 1:
            full_subnet_mask += "128"
            number_of_bits -= 1
        elif number_of_bits == 0:
            full_subnet_mask += "0"
            number_of_bits -= 0
    return str(full_subnet_mask)

def apply_mask(ip_address, subnet_mask):
    '''
    apply_mask(ip_address, subnet_mask) that returns a string
    Returns the subnet given an ip address and subnet mask.
    '''
    if verify_ip_address_format(ip_address) and verify_subnet_mask_format(subnet_mask):
        subnet_to_return = ""
        divided_ip_address = ip_address.split(".")
        divided_subnet_mask = subnet_mask.split(".")
        for current_division in range(4):
            ip_to_add = int(divided_ip_address[current_division])
            subnet_to_add = int(divided_subnet_mask[current_division])
            division_to_add = ip_to_add & subnet_to_add
            subnet_to_return += str(division_to_add)
            if not current_division == 3:
                subnet_to_return += "."
        return subnet_to_return
    return "invalid entry"

def check_resource(resource):
    '''
    check_resource(resource) that returns a boolean
    Returns True if the resource is valid.
    Returns False otherwise.
    '''
    ip_address = grab_ip_address(resource)
    subnet = grab_subnet(resource)
    regex_resource_string_full_subnet = re.compile(r'^/subnet\?[\d.]{7,15}&[\d.]{7,15}$')
    regex_resource_string_bit_subnet = re.compile(r'^/subnet\?[\d.]{7,15}&([0-2]?[0-9]|30|31)$')
    if regex_resource_string_full_subnet.search(resource) is None and regex_resource_string_bit_subnet.search(resource) is None:
        return False
    if not verify_ip_address_format(ip_address) or not verify_subnet_mask_format(subnet):
        return False
    return True

def check_resource_start(resource):
    '''
    check_resource_start(resource) that returns a boolean
    Returns True if the resource starts with '/subnet'.
    Returns False otherwise.
    '''
    regex_resource_start_string = re.compile(r'^/subnet')
    if regex_resource_start_string.search(resource) is None:
        return False
    return True

def grab_subnet(resource):
    '''
    grab_subnet(resource) that returns a string
    Returns the subnet mask string given the resource.
    '''
    regex_grab_subnet = re.compile(r'(?<=&)([\d.]{7,15}|[0-2]?[0-9]|30|31)$')
    if regex_grab_subnet.search(resource) is None:
        return '-1'
    return regex_grab_subnet.search(resource).group()

def grab_ip_address(resource):
    '''
    grab_ip_address(resource) that returns a string
    Returns the ip address string given the resource.
    '''
    regex_grab_ip = re.compile(r'(?<=\?)[\d.]{7,15}')
    if regex_grab_ip.search(resource) is None:
        return '-1'
    return regex_grab_ip.search(resource).group()

def grab_query(resource):
    '''
    grab_query(resource) that returns a string
    Returns the IP address and subnet mask string, seperated by '&'.
    '''
    regex_resource_string = re.compile(r'(?<=\?)[\d.]{7,15}&[\d.]{1,15}$')
    if regex_resource_string.search(resource) is None:
        return 'invalid entry'
    subnet = grab_subnet(resource)
    if is_subnet_mask_in_bit_format(subnet):
        return grab_ip_address(resource) + '&' + get_full_subnet_mask(subnet)
    return regex_resource_string.search(resource).group()
