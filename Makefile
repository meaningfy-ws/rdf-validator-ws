.PHONY: test install lint generate-tests-from-features

include compose/dev/api/.dev

BUILD_PRINT = \e[1;34mSTEP: \e[0m

#-----------------------------------------------------------------------------
# Basic commands
#-----------------------------------------------------------------------------

install-prod:
	@ echo "$(BUILD_PRINT)Installing the production requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements.txt

install-dev:
	@ echo "$(BUILD_PRINT)Installing the local requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements/dev.txt

test:
	@ echo "$(BUILD_PRINT)Running the tests"
	@ pytest

#-----------------------------------------------------------------------------
# API server related commands
#-----------------------------------------------------------------------------

build-dev-api:
	@ echo -e '$(BUILD_PRINT)Building the api container'
	@ docker-compose --file dev.yml --env-file compose/dev/api/.dev build validator-api

start-dev-api:
	@ echo -e '$(BUILD_PRINT)Starting the api container'
	@ docker-compose --file dev.yml --env-file compose/dev/api/.dev up -d validator-api

stop-dev-api:
	@ echo -e '$(BUILD_PRINT)Stopping the api container'
	@ docker-compose --file dev.yml --env-file compose/dev/api/.dev stop validator-api

#-----------------------------------------------------------------------------
# UI server related commands
#-----------------------------------------------------------------------------

build-dev-ui:
	@ echo -e '$(BUILD_PRINT)Building the ui container'
	@ docker-compose --file dev.yml --env-file compose/dev/ui/.dev build validator-ui

start-dev-ui:
	@ echo -e '$(BUILD_PRINT)Starting the ui container'
	@ docker-compose --file dev.yml --env-file compose/dev/ui/.dev up -d validator-ui

stop-dev-ui:
	@ echo -e '$(BUILD_PRINT)Stopping the ui container'
	@ docker-compose --file dev.yml --env-file compose/dev/ui/.dev stop validator-ui

#-----------------------------------------------------------------------------
# (all) Development environment
#-----------------------------------------------------------------------------

build-dev:
	@ echo -e '$(BUILD_PRINT)Building the dev container'
	@ docker-compose --file dev.yml --env-file compose/dev/api/.dev build

start-dev:
	@ echo -e '$(BUILD_PRINT)Starting the dev services'
	@ docker-compose --file dev.yml --env-file compose/dev/api/.dev up -d

stop-dev:
	@ echo -e '$(BUILD_PRINT)Stopping the dev services'
	@ docker-compose --file dev.yml --env-file compose/dev/api/.dev stop