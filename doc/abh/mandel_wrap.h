// This defines the signature of the function in mandel_wrap.f90.
// This is usually done in a header file as here but could be done in
// the .c file.  Neither are strictly necessary, see
// http://stackoverflow.com/questions/9182763/implicit-function-declarations-in-c

// Also about 2D arrays in functions:
// http://eli.thegreenplace.net/2010/04/06/pointers-vs-arrays-in-c-part-2d/
// i.e. they are not of type "int **"!

void c_calc_num_iter(int nre, double re[nre], int nim, double im[nim], int itermax, double escape, int out[nre][nim]);

// This also works but produces compiler warnings.  Note this is the
// type of signature used in the Julia and Matlab interface:
//void c_calc_num_iter(int nre, double re[nre], int nim, double im[nim], int itermax, double escape, int *out);

