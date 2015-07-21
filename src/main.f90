program chaos_commn
parameter (N=3,nosdata=40000)
implicit double precision (a-h,o-z)
double precision, dimension(nosdata) :: xt,xr,signal,recovered,encryptedx
double precision, dimension (N):: xold
tstep=0.0001;
ndrop=15000;
xold(1)=rand();
xold(2)=rand();
xold(3)=rand();
do i=1,ndrop
   call rkm_send(tstep,xold,N)
enddo
do i=1,nosdata
    call rkm_send(tstep,xold,N)
    xt(i)=xold(1);
enddo
do i=1,nosdata
   !signal(i)=rand()
   signal(i)=1.5*sin(0.01*float(i)) +1.0*sin(0.01*sqrt(2.0)*float(i))
enddo
do i=1,nosdata
   encryptedx(i)=signal(i)+xt(i);
enddo 
!renormscale(1)=minval(encryptedx,nosdata);
!renormscale(2)=maxval(encryptedx,nosdata);
!encryptedx=mynorm(encryptedx_pratik_speaker,normscale,numsample)';
!for i=1:numsample
!    encryptedx(i)=normscale(1)+(encryptedx_pratik_speaker(i)-renormscale(1))*(normscale(2)-normscale(1))/(renormscale(2)-renormscale(1));
!end    
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xold(1)=rand();
xold(2)=rand();
xold(3)=rand();
do i=1,ndrop
   call rkm_send(tstep,xold,N);
enddo 
do  i=1, nosdata
    call rkm_receive(tstep,xold,encryptedx(i),N);
    xr(i)=xold(1);
enddo
do i=1,nosdata
   recovered(i)=(encryptedx(i)-xr(i));
enddo
open (3,file="signal_recovered.dat")
do i=1,nosdata
   write(3,*)signal(i), recovered(i)
enddo
close(3)
end