#!/bin/bash

# This script runs locally

set -e

source tests/integration/kafka.sh

assert_count_equal_num_of_messages(){
  local count=$1
  local total_lines=$2

  if [ ! $count -eq $total_lines ]
  then
    echo "Failed assertion, there should be $total_lines messages but there were $count"
    exit 1
  fi
}

produce_entities(){
    echo "***** Produce entities *****"
    local total_lines=10
    local topic=entity-order
    local key=order_id
    local file=/tmp/orders.json

    echo "Create kafka topic"
    kafka_create_topic $topic

    echo "Create order file"
    create_order_file $file

    echo "Produce entities to topic"
    kafka_produce_topic $topic $file

    echo "Count number of messages"
    count="$(kafka_count_number_of_messages $topic $total_lines $key)"
    assert_count_equal_num_of_messages $count $total_lines
}

check_features(){
    echo "***** Check features *****"
    local topic=featuregroup-order_creation
    local total_lines=10
    local key=order_id

    echo "Consume features generated by transformation jobs"
    kafka_consume_topic $topic $total_lines $key

    echo "Count number of messages"
    count="$(kafka_count_number_of_messages $topic $total_lines $key)"
    assert_count_equal_num_of_messages $count $total_lines
}

main(){
  docker-compose down
  docker-compose up -d

  produce_entities
  check_features

  docker-compose down
}

main