program run_from_f
use fortran_mod
implicit none

integer:: a_int=5, ii
real(dp):: a_vec(5) = [3,4,6,78,99], a_array(3,4)=3.4, out(5,3)
a_array(1,1) = -10.5
a_array(2,1) = -100.5

out = fort_fun(a_int, a_vec, a_array)
do ii=1,size(out,1)
   print *, out(ii,:)
end do
end program run_from_f

