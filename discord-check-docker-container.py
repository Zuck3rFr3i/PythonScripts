# Dependencys: Docker, Discord
# Checks if a given Docker Container on the Same System is running and updates Discord Channel accordingly

running_containers = {
    "CONTAINER_NAME": {
        "chid": 1234,
        "activename": "🟢 | CONTAINER",
        "offname": "🔴 | CONTAINER",
        "state": 0
    },

    "CONTAINER_NAME": {
        "chid": 1234,
        "activename": "🟢 | CONTAINER",
        "offname": "🔴 | CONTAINER",
        "state": 0
    },

    "CONTAINER_NAME": {
        "chid": 1234,
        "activename": "🟢 | CONTAINER",
        "offname": "🔴 | CONTAINER",
        "state": 0
    }
}

class checkdocker_state():
    def isrunning(cname: str):
        docker_client = docker.from_env()
        RUNNING = "running"
        try:
            container = docker_client.containers.get(cname)
        except docker.errors.NotFound as exc: #Keeping this because a try needs a except
            pass
        else:
            container_state = container.attrs["State"]
            return container_state["Status"] == RUNNING



@tasks.loop(minutes=3)
async def checkinactive():
    for dcontainer in running_containers:
        status = checkdocker_state.isrunning(dcontainer)
        channel = client.get_channel(running_containers[dcontainer]["chid"])
        if status:
            if running_containers[dcontainer]["state"] == 0:
                running_containers[dcontainer]["state"] = 1
                await channel.edit(name=running_containers[dcontainer]["activename"])
        else:
            if running_containers[dcontainer]["state"] == 1:
                running_containers[dcontainer]["state"] = 0
                await channel.edit(name=running_containers[dcontainer]["offname"])  
