#!/usr/bin/env bash
set -euo pipefail
channel="${1:-can0}"
bitrate="${2:-1000000}"
[[ "$channel" =~ ^[a-zA-Z0-9_-]+$ ]] || { echo 'Invalid interface name' >&2; exit 2; }
[[ "$bitrate" =~ ^[0-9]+$ ]] && (( bitrate > 0 )) || { echo 'Invalid bitrate' >&2; exit 2; }
[[ "$(uname -s)" == Linux ]] || { echo 'Run on the Linux Pi host' >&2; exit 2; }
ip link show "$channel" >/dev/null
sudo ip link set "$channel" down
sudo ip link set "$channel" type can bitrate "$bitrate" restart-ms 0
sudo ip link set "$channel" up
ip -details -statistics link show "$channel"
