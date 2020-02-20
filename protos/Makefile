all:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. island.proto
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. battle.proto
	python -m grpc_tools.protoc -I. --python_out=. wade_messages.proto

install:
	sudo python -m pip install grpcio
	sudo python -m pip install grpcio-tools
