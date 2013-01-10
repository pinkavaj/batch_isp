all:
	python3 . \
		-sync 0 \
		-device ATxmega128A1 \
		-port /dev/ttyACM0 \
		-operation \
			MEMORY FLASH \
			ERASE F \
			READ \
			SAVEBUFFER dump.hex 386HEX

help:
	python3 . -h

sync:
	python3 . \
		-device ATxmega128A1 \
		-port /dev/ttyACM0
