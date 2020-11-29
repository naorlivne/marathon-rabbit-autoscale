# marathon-rabbit-autoscale
autoscale marathon services based on a rabbitmq queue size using a cronable metronome job
requires RabbitMQ’s HTTP Management API as it's the only sane way I've found to pull a queue length without forcing to declare the queue if it doesn't exists.

required envs:
* MIN_TASK_SIZE
* MAX_TASK_SIZE
* SCALE_EVERY_X_WAITING_MESSAGES
* RABBIT_HOST
* RABBIT_API_PORT (example: 15672)
* RABBIT_VHOST (example: /)
* RABBIT_QUEUE
* RABBIT_USER
* RABBIT_PASSWORD
* MARATHON_URL (example: leader.mesos for use inside mesos)
* MARATHON_PORT (example: 8080)
* MARATHON_APP

example metronome job config:
``````
{
  "id": "marathon-rabbit-autoscale",
  "run": {
    "cmd": "docker pull naorlivne/marathon-rabbit-autoscale:latest && docker run --rm -e MARATHON_APP=/app_name  -e MIN_TASK_SIZE=5 -e SCALE_EVERY_X_WAITING_MESSAGES=500 -e RABBIT_HOST=your_rabbit_host -e RABBIT_API_PORT=your_rabbit_api_port -e RABBIT_VHOST=your_rabbit_vhost -e RABBIT_PASSWORD=your_rabbit_pass -e RABBIT_USER=your_rabbit_user RABBIT_QUEUE=rabbit_queue_to_scale_by -e MARATHON_URL=leader.mesos -e MARATHON_PORT=8080 naorlivne/marathon-rabbit-autoscale:latest",
    "cpus": 0.1,
    "mem": 256,
    "disk": 100
  },
  "schedules": [
    {
      "id": "default",
      "enabled": true,
      "cron": "*/5 * * * *",
      "timezone": "UTC",
      "concurrencyPolicy": "ALLOW",
      "startingDeadlineSeconds": 30
    }
  ]
}
````````
