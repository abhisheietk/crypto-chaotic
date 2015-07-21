! Just runs it from Fortran. This can either be achieved by compiling
! it all together or with linking a precompiled shared lib see
! compile_so.sh.
program mandelbrot
use mandel
implicit none

!integer, parameter :: nre=31, nim=21
integer, parameter :: nre=3000, nim=10000
real(dp), parameter :: rer(2)=[-2._dp, 1._dp], imr(2)=[-1._dp,1._dp]
integer :: ii, jj, kk, out(nre,nim), itermax=99
real(dp) :: re(nre), im(nim), escape=2._dp
complex(dp) :: zz

! initialize
re = [ (dble(ii)/(nre-1)*(rer(2)-rer(1)) + rer(1) , ii=0, nre-1, 1) ]
im = [ (dble(ii)/(nim-1)*(imr(2)-imr(1)) + imr(1) , ii=0, nim-1, 1) ]

out = calc_num_iter(re, im, itermax, escape)

! ! plot array as x/y coordinates
! do jj=nim,1,-1
!    print '(30000I4.2)', out(:,jj)
! end do

end program mandelbrot
