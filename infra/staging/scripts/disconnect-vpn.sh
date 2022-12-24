#!/bin/bash
# NOTE: must have openvpn3 installed

generated_dir="$(dirname $(dirname $(realpath $0)) )/generated"
openvpn3 session-manage --config "$generated_dir/ovpn-config/user.ovpn" --disconnect