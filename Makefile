.PHONY: test install lint generate-tests-from-features

include .env.dev

BUILD_PRINT = \e[1;34mSTEP: \e[0m

#-----------------------------------------------------------------------------
# Basic commands
#-----------------------------------------------------------------------------

install-prod:
	@ echo "$(BUILD_PRINT)Installing the production requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements.txt

install-dev:
	@ echo "$(BUILD_PRINT)Installing the development requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements/dev.txt

test:
	@ echo "$(BUILD_PRINT)Running the tests"
	@ pytest

#-----------------------------------------------------------------------------
# API server related commands
#-----------------------------------------------------------------------------

build-dev-api:
	@ echo -e '$(BUILD_PRINT)Building the dev container'
	@ docker-compose --file docker-compose.dev.yml --env-file .env.dev build validator-api

run-dev-api:
	@ echo -e '$(BUILD_PRINT)Starting the dev services'
	@ docker-compose --file docker-compose.dev.yml --env-file .env.dev up validator-api -d

#-----------------------------------------------------------------------------
# (all) Development environment
#-----------------------------------------------------------------------------

build-dev:
	@ echo -e '$(BUILD_PRINT)Building the dev container'
	@ docker-compose --file docker-compose.dev.yml --env-file .env.dev build

run-dev:
	@ echo -e '$(BUILD_PRINT)Starting the dev services'
	@ docker-compose --file docker-compose.dev.yml --env-file .env.dev up -d

stop-dev:
	@ echo -e '$(BUILD_PRINT)Stopping the dev services'
	@ docker-compose --file docker-compose.dev.yml --env-file .env.dev down