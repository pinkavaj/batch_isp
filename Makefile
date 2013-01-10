all:
	python3 . \
		-sync 0 \
		-device ATxmega128A1 \
		-port /dev/ttyACM0 \
		-operation \
			MEMORY FLASH \
			READ \
			SAVEBUFFER dump.hex 386HEX
	#python3 . -device ATxmega128A1 -hardware RS232 -port /dev/ttyACM0 -operation bagr radlo aaa

help:
	python3 . -h

sync:
	python3 . \
		-device ATxmega128A1 \
		-port /dev/ttyACM0
