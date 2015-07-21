module fortran_mod_wrap
  use iso_c_binding, only: c_double, c_int
  use fortran_mod
  implicit none
contains
  ! need to make a subroutine as only scalars can be returned
  subroutine fort_fun_wrap(a_int, na_vec, a_vec, nia_array, nja_array, a_array, out) bind(c)
    integer(c_int), value, intent(in):: a_int, na_vec, nia_array, nja_array
    real(c_double), intent(in):: a_vec(na_vec), a_array(nja_array, nia_array) ! note the reversed indices
    real(c_double), intent(out):: out(nia_array, na_vec) ! note the reversed indices
    integer:: ii
    
    out = transpose(fort_fun(a_int, a_vec, transpose(a_array)))  ! the two transposes here to convert from/to C-array ordering
    ! print *, ' '
    ! print *, 'fort out:', size(out,1), size(out,2)
    ! do ii=1,size(out,1)
    !    print *, out(ii,:)
    ! end do
    ! print *, ' '

  end subroutine fort_fun_wrap
end module fortran_mod_wrap
