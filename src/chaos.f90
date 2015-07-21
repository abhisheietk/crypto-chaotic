
subroutine rkm_receive(h,x,xp,N)
implicit double precision (a-h,o-z)
double precision, dimension (N) :: x,xdot1, xdot2, xdot3, xdot4, g
hh=h*0.5;
call deriv_receive(xdot1,x,xp,N)
do i=1,N
    g(i)=x(i)+hh*xdot1(i);
enddo
call deriv_receive(xdot2,g,xp,N);
do i=1,N
    g(i)=x(i)+hh*xdot2(i);
enddo
call deriv_receive(xdot3,g,xp,N);
do i=1,N
    g(i)=x(i)+h*xdot3(i);
enddo
call deriv_receive(xdot4,g,xp,N);
do i=1,N
    x(i)=x(i)+h*(xdot1(i)+2.0*(xdot2(i)+xdot3(i))+xdot4(i))/6.0;
enddo
return
end
!*******************************************************************
subroutine rkm_send(h,x,N)
implicit double precision (a-h,o-z)
double precision, dimension (N) :: x,xdot1, xdot2, xdot3, xdot4, g
hh=h*0.5;
call deriv_send(xdot1,x,N);
do i=1,N
    g(i)=x(i)+hh*xdot1(i);
enddo
call deriv_send(xdot2,g,N);
do i=1,3
    g(i)=x(i)+hh*xdot2(i);
enddo
call deriv_send(xdot3,g,N);
do i=1,N
    g(i)=x(i)+h*xdot3(i);
enddo
call deriv_send(xdot4,g,N);
do i=1,N
    x(i)=x(i)+h*(xdot1(i)+2.0*(xdot2(i)+xdot3(i))+xdot4(i))/6.0;
enddo
return
end
!******************************************************************
subroutine deriv_receive(xdot,x,xp,N)
implicit double precision (a-h,o-z)
double precision, dimension (N) :: x,xdot
rho=25;
sigma=10;
beta=1.5;
xdot(1)=sigma*(x(2)-x(1));
xdot(2)=xp*rho-x(2)-xp*x(3);
xdot(3)=xp*x(2)-beta*x(3);
return
end
!*********************************************************************
subroutine deriv_send(xdot,x,N)
implicit double precision (a-h,o-z)
double precision, dimension (N) :: x,xdot 
rho=25;
sigma=10;
beta=1.5;
xdot(1)=sigma*(x(2)-x(1));
xdot(2)=x(1)*rho-x(2)-x(1)*x(3);
xdot(3)=x(1)*x(2)-beta*x(3);
return
end
!***********************************************************************