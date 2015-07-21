module mandel_wrap
  ! To wrap calc_num_iter for use in C using iso_c_binding

  use iso_c_binding, only: c_double, c_int
  use mandel, only:  calc_num_iter

  implicit none

contains

  ! need to make a subroutine as only scalars can be returned
  subroutine c_calc_num_iter(nre, re, nim, im, itermax, escape, out) bind(c)
    real(c_double), intent(in):: re(nre), im(nim)
    real(c_double), intent(in), value:: escape
    integer(c_int), intent(in), value:: itermax, nre, nim
    integer(c_int), intent(out):: out(nim, nre)  ! note that in C the indices will be reversed!
    out = transpose(calc_num_iter(re, im, itermax, escape))  ! thus the transpose here!
  end subroutine c_calc_num_iter

  subroutine c_calc_num_iter2(re, im, itermax, escape, out) bind(c)
    real(c_double), intent(in):: re(:), im(:)
    real(c_double), intent(in), value:: escape
    integer(c_int), intent(in), value:: itermax
    integer(c_int), intent(out):: out(size(im), size(re))  ! note that in C the indices will be reversed!
    out = transpose(calc_num_iter(re, im, itermax, escape))  ! thus the transpose here!
  end subroutine c_calc_num_iter2

end module mandel_wrap


