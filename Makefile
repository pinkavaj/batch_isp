all:
	python3 . \
		-sync 0 \
		-device ATxmega128A1 \
		-port /dev/ttyACM0 \
		-operation \
			ERASE F \
			BLANKCHECK \
			MEMORY FLASH \
			LOADBUFFER test_prg/test00.hex \
			PROGRAM \
			START RESET 0

read:
	python3 . \
		-sync 0 \
		-device ATxmega128A1 \
		-port /dev/ttyACM0 \
		-operation \
			MEMORY FLASH \
			READ \
			SAVEBUFFER dump.hex 386HEX

reset:
	python3 . \
		-device ATxmega128A1 \
		-port /dev/ttyACM0 \
		-operation \
			START RESET 0

help:
	python3 . -h

sync:
	python3 . \
		-device ATxmega128A1 \
		-port /dev/ttyACM0
