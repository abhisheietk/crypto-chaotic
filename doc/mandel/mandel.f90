! Calculates the Mandelbrot set
module mandel
  implicit none

  integer, parameter :: dp=kind(0.d0) ! double precision

contains
  
  pure function mandel_frac(z, c) result(out)
    ! The Mandelbrot map: z -> z^2 + c
    complex(dp), intent(in):: z, c
    complex(dp):: out  
    out = z**2 + c
  end function mandel_frac

  function calc_num_iter(re, im, itermax, escape) result(out)
    ! Iterates on mandel_frac
    ! Input: 
    !  - re/im: vector of real/imaginary values of grid
    !  - itermax: maximum of iterations done
    !  - escape: stops if abs(z)>escape, for Mandelbrot escape=2
    ! Output:
    !  - number of iterations until abs(z)>escape
    real(dp), intent(in):: re(:), im(:), escape
    integer, intent(in):: itermax
    integer:: out(size(re), size(im))
    integer:: ii, jj, kk, itt
    complex(dp):: zz, cc

    !$OMP PARALLEL  PRIVATE(jj, zz, cc, itt, kk)

    !$OMP DO
    do jj=1,size(im)
       do ii=1,size(re) 
          zz = 0
          cc = cmplx(re(ii), im(jj), dp)
          do kk=1,itermax
             zz = mandel_frac(zz, cc)
             if (abs(zz)>escape) then
                exit
             end if
          end do
          if (kk>=itermax) then
             out(ii,jj) = -1
          else
             out(ii,jj) = kk
          end if
       end do
    end do
    !$OMP END PARALLEL  

  end function calc_num_iter

end module mandel


