/*
 * D.Béréziat (c) 2011-2021 Sorbonne Université
 *
 * Example of reading, processing and writing image with the Imlib2 library.
 * Installation on Ubuntu/Debian, type in a terminal:
 *   sudo apt-get install libimlib2-dev
 * Installation on OSX with Homebrew:
 *   - installation of homebrew: type in a terminal: 
 *      curl /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
 *   - installation of the library:
 *      brew install imlib2
 * Compilation:
 *   gcc imlib-example.c -o imlib-example `imlib2-config --cflags --libs`
 * or:
 *   make
 */

#include <Imlib2.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/*
 * Read an image (of any type) and convert to grayscale
 */
unsigned char * read_grayscale(char *fname, int *dimx, int *dimy)
{
    Imlib_Image *image;

    image = (Imlib_Image *)imlib_load_image(fname);
    if(image)
    {
        unsigned char *buf, *data;
        int l,c;

        imlib_context_set_image( image);
        *dimx = imlib_image_get_width();
        *dimy = imlib_image_get_height();
        data  = (unsigned char *)imlib_image_get_data();
        buf = (unsigned char*) malloc(sizeof(char)**dimx**dimy);
        for(l=0;l<*dimy;l++)
	  for(c=0;c<*dimx;c++)
            {
                *buf++ = (*data + *(data+1) + *(data+2))/3;
                data += 4;
            }
        imlib_free_image();
        return buf-*dimx**dimy;
    }
    else
    {
        fprintf( stderr, "Error: image %s not read.\n", fname);
        exit(33);
    }
}

/*
 * Write an image. The filename extension gives the image format. For instance,
 * to write in a PNG format: 'myimage.png'.
 */

void write_grayscale(char *fname, int dimx, int dimy, unsigned char *buf)
{
    Imlib_Image *image;
    unsigned char *data;
    int l, c;
    char *ext;

    if( !(ext = strchr( fname, '.')))
    {
        fprintf( stderr, "Error: format image unknown\n");
        exit(34);
    }

    data = (unsigned char *)malloc(sizeof(char)*dimx*dimy*4);
    for( l=0; l<dimy; l++)
      for( c=0; c<dimx; c++)
        {
            *data = *buf;
            *(data+1)= *buf;
            *(data+2) = *buf;
            *(data+3) = 0;
            buf ++; data += 4;
        }
    data -= dimx*dimy*4;
    image = (Imlib_Image *)imlib_create_image_using_data( dimx, dimy, (DATA32*)data);
    imlib_context_set_image( image);
    imlib_image_set_format(ext+1);
    imlib_save_image( fname);
    imlib_free_image();
    free( data);
}

/*
 * An example with a basic process
 */

void process_image();


int main(int argc, char **argv)
{
    char *inName, *outName;
    double seuil;
    if(argc > 3)
    {
        unsigned char *buf_in, *buf_out;
        int dimx, dimy; /* number of image row and line */
        int x, y;

        /* command parameters */
        inName=argv[1];
        outName=argv[2];
        seuil = atof(argv[3]);
        
        /* read the image */
        buf_in = read_grayscale(inName, &dimx, &dimy);

        /* process the image */
        buf_out = (unsigned char *)malloc(dimx*dimy);
        process_image(buf_out, buf_in, dimx, dimy, seuil);

        /* write the image */
        write_grayscale(outName, dimx, dimy, buf_out);
        
        free(buf_in);
        free(buf_out);
    }
    else
        printf("Usage: %s image-in image-out threshold\n", *argv);
    return 0;
}

/* Example with an image  thresholding
 */

void process_image (unsigned char *buf_out, unsigned char *buf_in, int dimx, int dimy, double seuil)
{
    int i, j;
    for(j=0;j<dimy;j++)
        for(i=0;i<dimx;i++)
	  buf_out[i+dimx*j]= (buf_in[i+dimx*j] > seuil)*255;
  
}

/**
 * Write a color (RGB) image.
 */

void write_color(char *fname, int dimx, int dimy, unsigned char *R, unsigned char *G, unsigned char *B) {
  Imlib_Image *image;
  unsigned char *data;
  char *ext;
  int l;
  
  if( !(ext = strchr( fname, '.'))) {
    fprintf( stderr, "Erreur: format image non reconnu\n");
    exit(34);
  }
  
  data = (unsigned char *)malloc(sizeof(char)*dimx*dimy*4);
  if( !data) {
    fprintf( stderr, "Erreur: plus de memoire libre (allocation de %ld octets).\n",
	     dimx*dimy*sizeof(float));
    exit(36);
  }
  for( l=0; l<dimy; l++) {
    int c;
    for( c=0; c<dimx; c++) {
      *data = *R++;
      *(data+1)= *G++;      *(data+2) = *B++;
      *(data+3) = 0;
      data += 4;
    }
  }
  data -= dimx*dimy*4;
  image = imlib_create_image_using_data( dimx, dimy, (DATA32*)data);
  imlib_context_set_image( image);
  imlib_image_set_format( ext+1);
  imlib_save_image( fname);
  imlib_free_image();
  free( data);  
}
