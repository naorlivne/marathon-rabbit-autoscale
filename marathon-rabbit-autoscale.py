import os, requests
from pyrabbit.api import Client

min_task_size = os.environ["MIN_TASK_SIZE"]
scale_every_x_waiting_messages = os.environ["SCALE_EVERY_X_WAITING_MESSAGES"]
rabbit_host = os.environ["RABBIT_HOST"]
rabbit_api_port = os.environ["RABBIT_API_PORT"]
rabbit_vhost = os.environ["RABBIT_VHOST"]
rabbit_password = os.environ["RABBIT_PASSWORD"]
rabbit_user = os.environ["RABBIT_USER"]
rabbit_queue = os.environ["RABBIT_QUEUE"]
marathon_url = os.environ["MARATHON_URL"]
marathon_port = os.environ["MARATHON_PORT"]
marathon_app = os.environ["MARATHON_APP"]

# marathon connections strings
url = "http://" + marathon_url + ":" + marathon_port + "/v2/apps" + marathon_app
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

# connect to rabbit
rabbit_connection = Client(rabbit_host + ":" + rabbit_api_port, rabbit_user, rabbit_password)
print "connected to rabbit"

# get rabbit queue size and figure out amount of tasks needed
rabbit_size = rabbit_connection.get_queue_depth(rabbit_vhost, rabbit_queue)
workers_needed = int(int(rabbit_size)/int(scale_every_x_waiting_messages))
if workers_needed < int(min_task_size):
    workers_needed = int(min_task_size)

# get current number of tasks
response = requests.request("GET", url, headers=headers)
app_data = response.json()

# if current number is different then required number change it to required number
if int(app_data["app"]["instances"]) != int(workers_needed):
    print "scaling from " + str(app_data["app"]["instances"]) + " to " + str(workers_needed) + " workers"
    payload = "{\"instances\": " + str(workers_needed) + "}"

    response = requests.request("PUT", url, data=payload, headers=headers)
    print response.text
else:
    print "no rescaling needed"
