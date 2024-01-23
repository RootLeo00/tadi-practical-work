
imlib-example: imlib-example.c
	gcc $^ -o $@ `imlib2-config --cflags --libs` -I/opt/X11/include
test:
	./imlib-example olena.jpg output.jpg 150
	if [ `uname` = Linux ]; then xdg-open sortie.jpg; else open sortie.jpg; fi

clean:
	rm imlib-example

.PHONY: test clean
