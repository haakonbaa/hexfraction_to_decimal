// Bruk 'g++ savepng.cpp -o savepng -lpng' !

#include <png.h>
#include <functional>
#include <math.h>


// HSV til RGB tatt fra https://stackoverflow.com/questions/3018313/algorithm-to-convert-rgb-to-hsv-and-hsv-to-rgb-in-range-0-255-for-both
typedef struct {
    double r;       // a fraction between 0 and 1
    double g;       // a fraction between 0 and 1
    double b;       // a fraction between 0 and 1
} rgb;

typedef struct {
    double h;       // angle in degrees
    double s;       // a fraction between 0 and 1
    double v;       // a fraction between 0 and 1
} hsv;

static rgb   hsv2rgb(hsv in);

rgb hsv2rgb(hsv in)
{
    double      hh, p, q, t, ff;
    long        i;
    rgb         out;

    if(in.s <= 0.0) {       // < is bogus, just shuts up warnings
        out.r = in.v;
        out.g = in.v;
        out.b = in.v;
        return out;
    }
    hh = in.h;
    if(hh >= 360.0) hh = 0.0;
    hh /= 60.0;
    i = (long)hh;
    ff = hh - i;
    p = in.v * (1.0 - in.s);
    q = in.v * (1.0 - (in.s * ff));
    t = in.v * (1.0 - (in.s * (1.0 - ff)));

    switch(i) {
    case 0:
        out.r = in.v;
        out.g = t;
        out.b = p;
        break;
    case 1:
        out.r = q;
        out.g = in.v;
        out.b = p;
        break;
    case 2:
        out.r = p;
        out.g = in.v;
        out.b = t;
        break;

    case 3:
        out.r = p;
        out.g = q;
        out.b = in.v;
        break;
    case 4:
        out.r = t;
        out.g = p;
        out.b = in.v;
        break;
    case 5:
    default:
        out.r = in.v;
        out.g = p;
        out.b = q;
        break;
    }
    return out;     
}

//const double PI = 3.141592653589793238264;

void CREATE_PNG(const char*, int, int, std::function<void(int,int,float[4])>);
float map(float,float,float,float,float);

const int MAXITERS = 300; // Maximalt antall ntall iterasjoner for hvert komplekse tall. 

int main(int argc, char *argv[]) {

    CREATE_PNG("fractal.png",1920,1920,[&](int width, int height, float* color) {

        float cr = map(width,0,1920,-2,0.6);//std::cos(ANGLE);
        float ci = map(height,0,1920,1.3,-1.3);//std::sin(ANGLE);/


        float zr = 0;//map(width,0,1920,-1.3,1.3);
        float zi = 0;//map(height,0,1920,1.3,-1.3);

        float zr_next;
        float zi_next;

        float radius = 0;
        unsigned int iters = 0;

        // (zr+zi)^2 = (zr)^2+2*zr*zi-(zi)^2

        while (radius <= 16) {

            zr_next = (zr*zr)-(zi*zi)+cr;
            zi_next = (2*zr*zi)+ci;

            zr = zr_next;
            zi = zi_next;

            iters++;
            radius = zr*zr+zi*zi; // radius^2
            if (iters == MAXITERS) {
                break;
            }
        }

        float dist = map(iters,0,100,0,360);
        hsv from_color = {dist,1,1};
        rgb to_color = hsv2rgb(from_color);

        if (iters == MAXITERS) {
            color[0] = 0;
            color[1] = 0;
            color[2] = 0;
        } else {
            color[0] = to_color.r;
            color[1] = to_color.g;
            color[2] = to_color.b;
        }
        color[3] = 1;
    });

    return 0;
}

float map(float n,float min,float max,float rmin,float rmax) {
    return ((n-min)/(max-min))*(rmax-rmin)+rmin;
}

/*
 * Dette er den eneste funskjonen som trengs for å lagre et bilde. Legg merke til hvordan
 * Lambda-funskjonen fungerer!
 * 
 * Lambdafunskjonen tar å gir hver eneste piksel en farge:
 * std::function<void(int width,int height ,float[4] color)>
 * 
 * float[4] color; spesifiserer en farge med R,G,B,A verdier.
 */
void CREATE_PNG(const char* filename, int width, int height, std::function<void(int,int,float[4])> map_func) {

    // Reserver minne
    png_bytep *row_pointers = NULL;
    row_pointers = (png_bytep*)malloc(sizeof(png_bytep) * height);
    for(int y = 0; y < height; y++) {
        row_pointers[y] = (png_byte*)malloc(sizeof(png_bytep) * width );
    }
    
    // Sriv data til minnet
    float color[4] = {};
    for(int y = 0; y < height; y++) {
        png_bytep row = row_pointers[y];
        for(int x = 0; x < width; x++) {
            png_bytep px = &(row[x * 4]);
            map_func(x,y,color);
            px[0] = (unsigned char)(std::ceil(255*color[0]-0.5));
            px[1] = (unsigned char)(std::ceil(255*color[1]-0.5));
            px[2] = (unsigned char)(std::ceil(255*color[2]-0.5));
            px[3] = (unsigned char)(std::ceil(255*color[3]-0.5));
        }
    }

    // Åpne fila
    FILE *fp = fopen(filename, "wb");
    if(!fp) abort();

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if (!png) abort();

    png_infop info = png_create_info_struct(png);
    if (!info) abort();

    if (setjmp(png_jmpbuf(png))) abort();

    png_init_io(png, fp);

    //Bildet har bitdypde; 8 og RGBA-format.
    png_set_IHDR(
        png,
        info,
        width, height,
        8,
        PNG_COLOR_TYPE_RGBA,
        PNG_INTERLACE_NONE,
        PNG_COMPRESSION_TYPE_DEFAULT,
        PNG_FILTER_TYPE_DEFAULT
    );
    png_write_info(png, info);
    if (!row_pointers) abort();

    // Skriv data til bildet
    png_write_image(png, row_pointers);
    png_write_end(png, NULL);

    // Frigjør minne.
    for(int y = 0; y < height; y++) {
        free(row_pointers[y]);
    }
    free(row_pointers);
    fclose(fp);
    png_destroy_write_struct(&png, &info);
}

/*
 * This code is originally from:
 * http://zarb.org/~gc/html/libpng.html
 *
 * Modified by Yoshimasa Niwa (and others) to make it much simpler
 * and support all defined color_type.
 *
 * Copyright 2002-2010 Guillaume Cottenceau.
 *
 * This software may be freely redistributed under the terms
 * of the X11 license.
 *
 */