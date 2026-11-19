---
created: 2026-09-26
---

# Introduction to Docker

## Virtualization
Creating a new system inside an existing system by using the resources of the original system.

### Hypervisor
Divides resources and allocates them to virtual environments, so you can run multiple operating systems on the same computer.


## Docker
Docker runs **containers**, which are lightweight, isolated environments on your system.

### Dockerfile
```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y coffee-maker
COPY . /coffee-recipe
RUN ./prepare-beans.sh
CMD ["./brew-coffee.sh"]
```

- A **Dockerfile** creates a Docker **image**.
- `CMD` is the command the container runs by default.
- Images are immutable — you can't change them, only rebuild.

### Building a Docker Image
Docker tags new images as `latest` by default.

```shell
docker build -t my-image .
```

To check images and run a container:
```shell
docker images
docker run my-image
```

- To change an image, rebuild it (optionally with a new tag).

## How Docker Differs from Hypervisors
- Hypervisors virtualize **hardware** (full guest OS per VM).
- Docker virtualizes the **OS layer** (containers share the host kernel).



