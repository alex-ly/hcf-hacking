.PHONY: all run shell

IMAGE                = hcf/designer-notebook
OPT                  = --rm -it -p 8001:8001

all:
	docker build -t $(IMAGE) .

run:
	docker run $(OPT) \
		--name designer \
		-v $(PROBLEMSETS):/home/jovyan/problemsets \
		-v $(EXCHANGE):/home/jovyan/exchange \
		-v $(PWD)/config:/etc/jupyter \
		-v $(PWD)/dot-jupyter:/home/jovyan/.jupyter \
		-v $(PWD)/tools:/srv/tools \
		$(IMAGE)

shell:
	docker exec -it designer /bin/bash
