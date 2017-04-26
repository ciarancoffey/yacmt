#!/usr/bin/env bats

@test "nginx is installed" {
    result="$(dpkg -l nginx >/dev/null; echo $?)"
    [ "$result" -eq 0 ]
}

@test "nano is uninstalled" {
    result="$(dpkg -l nano >/dev/null; echo $?)"
    [ "$result" -ne 0 ]
}

@test "nginx config exists" {
    result="$([ -f /etc/nginx/sites-available/default ] ; echo $?)"
    [ "$result" -eq  0 ]
}

@test "nginx config is enabled, as a symlink" {
    result="$([ -h /etc/nginx/sites-enabled/default ] ; echo $?)"
    [ "$result" -eq  0 ]
}

@test "nginx config is correct" {
    result="$(md5sum /etc/nginx/sites-available/default | cut -f 1 -d " " )"
    [ "$result" ==  039ffab8c4f37b7061c4baa7e1b53667 ]
}
