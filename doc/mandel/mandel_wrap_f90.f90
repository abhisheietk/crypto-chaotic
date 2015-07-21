module mandel_wrap_f90
  ! To wrap calc_num_iter into a subroutine for use in Julia without
  ! the use of iso_c_binding

  use mandel, only:  calc_num_iter, dp

  implicit none
contains
  ! need to make a subroutine as only scalars can be returned
  subroutine f90_calc_num_iter(nre, re, nim, im, itermax, escape, out) bind(c)  ! the bind(c) avoids name mangling in shared lib
    real(dp), intent(in):: re(nre), im(nim)
    real(dp), intent(in):: escape
    integer, intent(in):: itermax, nre, nim
    integer, intent(out):: out(nre, nim)
    out = calc_num_iter(re, im, itermax, escape)  
  end subroutine f90_calc_num_iter
end module mandel_wrap_f90

