GRPC_OUTPUT = .

PROTO_DIR = ./proto
PROTO_FILES = $(shell find $(PROTO_DIR) -type f -name '*.proto')

.PHONY: grpc
grpc:
	poetry run python -m grpc_tools.protoc -I $(PROTO_DIR) --python_out=$(GRPC_OUTPUT) --grpc_python_out=$(GRPC_OUTPUT) $(PROTO_FILES)
