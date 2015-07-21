#include <stdio.h>
#include <math.h>
#define NI 5
#define NJ 3
#define NK 4

int main ( void ) {
  double out[NI][NJ];
  int a_int=5, ii, jj;
  double a_vec[NI]  = {3,4,6,78,99}, a_array[NJ][NK]={[0 ... NJ-1][0 ... NK-1] = 3.4};
  a_array[0][0] = -10.5;
  a_array[1][0] = -100.5;
  /* for (ii=0; ii<NJ; ii++){ */
  /*   for (jj=0; jj<NK; jj++){ */
  /*     a_array[ii][jj] = (double)ii + ((double)jj)/10.; */
  /*   }} */
  /* for (ii=0; ii<NJ; ii++){ */
  /*   for (jj=0; jj<NK; jj++){ */
  /*     printf(" %f ",a_array[ii][jj]); */
  /*   } */
  /*   printf("\n"); */
  /* } */
  /*   printf("\n"); */

  // call to fortran
  fort_fun_wrap(a_int,NI, a_vec, NJ, NK, a_array, out);
    
  // print result
  for (ii=0; ii<NI; ii++){
    for (jj=0; jj<NJ; jj++){
      printf(" %f ",out[ii][jj]);
    }
    printf("\n");
  }
  return 0;
}
