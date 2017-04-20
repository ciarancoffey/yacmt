#!/usr/bin/env bats

@test "Host is listening on :80" {
    result="$(nc localhost 80 -z; echo $?)"
    [ "$result" -eq 0 ]
}

@test "Host responds with 200 OK on :80" {
    result="$(curl -s -o /dev/null -w "%{http_code}" localhost)"
    [ "$result" -eq 200 ]
}

@test "Host responds with Hello, World" {
    result="$(curl -s localhost)"
    [ "$result" = "Hello, world!" ]
}
