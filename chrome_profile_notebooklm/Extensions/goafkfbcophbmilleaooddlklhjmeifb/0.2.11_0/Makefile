PROJECT_DIR := $(CURDIR)
MANIFEST_FILE := $(PROJECT_DIR)/manifest.json
BUILD_DIR := $(PROJECT_DIR)/build
REACT_DIR := $(PROJECT_DIR)/react
ZIP_NAME := $(shell grep '"version":' $(MANIFEST_FILE) | awk -F '"' '{print "$(BUILD_DIR)/SyntheticFi_"$$4".zip"}')

include $(REACT_DIR)/.env.sentry-build-plugin

.PHONY: build clean

# Default target
build: clean npm_build $(BUILD_DIR) $(ZIP_NAME)

npm_build:
	@echo "Running npm run build in $(REACT_DIR)"
	cd $(REACT_DIR) && npm run build

# Ensure the build directory exists
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Create the zip file, excluding node_modules
$(ZIP_NAME): $(BUILD_DIR)
	@echo "Creating zip file: $(ZIP_NAME)"
	zip -r $(ZIP_NAME) . -x "node_modules/*" "*/node_modules/*" ".git/*" ".DS_Store"
	@echo "Zip file created: $(ZIP_NAME)"

# Clean up the build directory
clean:
	@rm -rf $(BUILD_DIR)
	@echo "Build directory cleaned."