all:
	#python3 . -device ATxmega128A1 -hardware RS232 -port /dev/ttyACM0 -operation bagr radlo aaa
	python3 . -device ATxmega128A1 -port /dev/ttyACM0 -operation bagr radlo aaa
