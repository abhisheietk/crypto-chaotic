% This uses Matlab's loadlibrary and calllib to directly call the wrapped function.  It
% does some magic with returning all the pointer variables so if they get modified they
% can be used again.
%
% This apporach is essentially the same as Julia's and python-cffi, except Matlab does the
% parsing of the h-file for you.  Sadly Octave does not yet support this at all.  Bindings
% could also be done with SWIG or through MEX-files:
% https://publicwiki.deltares.nl/display/OET/Matlab+interfacing+fortran

% Matlab reference:
% http://www.mathworks.co.uk/help/matlab/ref/loadlibrary.html#btjfvd3

%libname = 'libmandel_colmajor';
libname = 'libmandel_colmajor_openMP'; % openMP works
[notfound,warnings]=loadlibrary(libname, 'mandel_wrap_colmajor4matlab.h');

nn = 1000;
ni = 1100;
re = linspace(-2.1,1,nn);
im = linspace(-1.3,1.3,ni);
itermax = 20;
escape = 2.0;
result = zeros(nn, ni)-5;

tic
[re, im, result] = calllib(libname, 'f_calc_num_iter', nn, re, ni, im, itermax, escape, result);
toc

imagesc(result);

