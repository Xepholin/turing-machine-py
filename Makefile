##
# Turing Machine Python
#

run:
	python3 src/main.py calc abbbaaaa MT_code/test
	python3 src/main.py link 1110001 MT_code/rightleft MT_code/left1

clean:
	-rm -r src/__pycache__

# End