module fortran_mod
  implicit none

  integer, parameter :: dp=kind(0.d0) ! double precision

contains
  pure function fort_fun(a_int, a_vec, a_array) result(out)
    integer, value, intent(in):: a_int
    real(dp), intent(in):: a_vec(:), a_array(:,:)
    integer:: ii, jj
    real:: out(size(a_vec), size(a_array,1))
    do ii=1,size(a_vec) ! fill out with some combination of input
       out(ii,:) = a_vec(ii) + sum(a_array,2) + dble(a_int)
    end do
  end function fort_fun
end module fortran_mod



