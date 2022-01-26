function gridsurf2mat(inputname,outputname)

[x,y,z]=textread(inputname,'%f %f %f');
c=find(abs(z)>=1E+32);
z(c)=nan;
xu=unique(x);yu=unique(y);
nx=length(xu);ny=length(yu);
if x(1)==x(2)
    X=reshape(x,ny,nx);
    Y=reshape(y,ny,nx);
    Z=reshape(z,ny,nx);
else
    X=reshape(x,nx,ny);
    Y=reshape(y,nx,ny);
    Z=reshape(z,nx,ny);   
end
tipe='kontur';
save(outputname,'X','Y','Z','tipe')


