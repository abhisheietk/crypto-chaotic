// This calls the wrapped function from mandel_wrap.f90 from c.  This
// can either be achieved by compiling it all together or with
// linking a precompiled shared lib see compile_so.sh.
#include <stdio.h>
#include "mandel_wrap.h"

/* #define NRE 31 */
/* #define NIM 21 */
#define NRE 10000
#define NIM 2000

// globals go on the heap.  Locals go on the stack and will result in
// a stackoverflow if they get too big.
int res[NRE][NIM];  
double re[NRE], im[NIM];


//void c_calc_num_iter(int nre, double re[nre], int nim, double im[nim], int itermax, double escape, int out[nre][nim]);

void printvec (int ni, double *ii){
  int i;
  for (i=0; i<ni; i++){
    printf(" %4.1f ",ii[i]);
  }
  printf("\n");
}

// prints the array to screen as x/y coordinates
void printarr(int ni, int nj, int arr[NRE][NIM], double *ii, double *jj){
  int i, j;
  printf("\n");
  printf(" y\\x   ");
  printvec(ni, ii);

  for (j=nj-1; j>=0; j--){
    printf(" %4.1f ",jj[j]);
    for (i=0; i<ni; i++){
      printf(" %4d ",arr[i][j]);
    }
    printf("\n");
  }
  printf("\n");
}


int main ( void ) {
  int i, j, itermax=99;
  int nre=NRE, nim=NIM;
  double escape=2., dx, dy;
  // NOTE: index not reversed!
  // make real and imaginary vectors
  dx = 3.0/(NRE-1);
  re[0] = -2.;
  for (i=1; i<NRE; i++)
    re[i] = re[i-1] + dx;
  dy = 2.0/(NIM-1);
  im[0] = -1.;
  for (i=1; i<NIM; i++){
    im[i] = im[i-1] + dy;
    if (im[i]<1e-6 && im[i]>-1e-6)
      im[i] = 0.; // otherwise result is not equal to Fortran's
  }
  //printvec(NRE, re);
  //printvec(NIM, im);

  // Call to fortran:
  c_calc_num_iter(NRE, re, NIM, im, itermax, escape, res);
    
  // print result
  //printarr(NRE, NIM, res, re, im);
  return 0;
}
