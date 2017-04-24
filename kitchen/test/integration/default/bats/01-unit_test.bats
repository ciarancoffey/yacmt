#!/usr/bin/env bats

@test "nginx is installed" {
    result="$(dpkg -l nginx >/dev/null; echo $?)"
    [ "$result" -eq 0 ]
}

@test "nano is uninstalled" {
    result="$(dpkg -l nano >/dev/null; echo $?)"
    [ "$result" -ne 0 ]
}
