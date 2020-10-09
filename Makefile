.PHONY: test install lint generate-tests-from-features

include docker/.env

BUILD_PRINT = \e[1;34mSTEP: \e[0m

#-----------------------------------------------------------------------------
# Basic commands
#-----------------------------------------------------------------------------

install-dev:
	@ echo "$(BUILD_PRINT)Installing the local requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements/dev.txt

install-prod:
	@ echo "$(BUILD_PRINT)Installing the production requirements"
	@ pip install --upgrade pip
	@ pip install -r requirements.txt

test:
	@ echo "$(BUILD_PRINT)Running the tests"
	@ pytest

dev:
	@ echo -e '$(BUILD_PRINT)Building the api container'
	@ docker-compose --file dev.yml --env-file docker/.env build validator-api
	@ echo -e '$(BUILD_PRINT)Building the ui container'
	@ docker-compose --file dev.yml --env-file docker/.env build validator-ui

prod:
	@ echo -e '$(BUILD_PRINT)Building the api container'
	@ docker-compose --file prod.yml --env-file docker/.env build validator-api
	@ echo -e '$(BUILD_PRINT)Building the ui container'
	@ docker-compose --file prod.yml --env-file docker/.env build validator-ui

start-dev:
	@ echo -e '$(BUILD_PRINT)Starting the api container'
	@ docker-compose --file dev.yml --env-file docker/.env up -d validator-api
	@ echo -e '$(BUILD_PRINT)Starting the ui container'
	@ docker-compose --file dev.yml --env-file docker/.env up -d validator-ui

stop-dev:
	@ echo -e '$(BUILD_PRINT)Stopping the ui container'
	@ docker-compose --file dev.yml --env-file docker/.env stop validator-ui
	@ echo -e '$(BUILD_PRINT)Stopping the api container'
	@ docker-compose --file dev.yml --env-file docker/.env stop validator-api

start-prod:
	@ echo -e '$(BUILD_PRINT)Starting PRODUCTION the api container'
	@ docker-compose --file prod.yml --env-file docker/.env up -d validator-api
	@ echo -e '$(BUILD_PRINT)Starting the ui container'
	@ docker-compose --file prod.yml --env-file docker/.env up -d validator-ui

stop-prod:
	@ echo -e '$(BUILD_PRINT)Stopping  PRODUCTION the ui container'
	@ docker-compose --file prod.yml --env-file docker/.env stop validator-ui
	@ echo -e '$(BUILD_PRINT)Stopping the api container'
	@ docker-compose --file prod.yml --env-file docker/.env stop validator-api