all:
	python3 . \
		-sync 0 \
		-device ATxmega128A1 \
		-port /dev/ttyACM0 \
		-operation \
			ERASE F \
			BLANKCHECK \
			MEMORY FLASH \
			LOADBUFFER dump_flash.hex \
			PROGRAM \
			READ \
			SAVEBUFFER dump.hex 386HEX

help:
	python3 . -h

sync:
	python3 . \
		-device ATxmega128A1 \
		-port /dev/ttyACM0
