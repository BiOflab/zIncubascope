clear all
Vid=VideoReader('Composite-1-80.avi');


Vid_Mask= tiffreadVolume('MASK_Composite-2-1-2.tif');

% VideoReader('MASK_hypoosmotic shock.avi');

% V_m=read(Vid,1);

folder_save='C:\Users\Anirban\Desktop\Incubascope Data\composite2\FOR PAPER';
% Im_mask=load("Im_final_mask_store.mat");

% Vid_Mask=Im_mask.Im_final_mask_store;



%%
st=1;
tic

lim_lumen=65;
rot_start=0;
rot_end=360;
gap=40;

frame_interval=5;
rot_interval=5;

V_rot_temp= [0;0] ;
for fr=1:frame_interval:50
    n=fr;
V=read(Vid,fr);
V=squeeze(V(:,:,1));

f=figure;

for rot=rot_start:rot_interval:rot_end

Im=V;
Im=imrotate(Im,rot,'crop');

BWs=Vid_Mask(:,:,fr);
% BWs=read(Vid,fr);
% BWs=squeeze(BWs(:,:,1));

BWs=imrotate(BWs,rot,'crop');

se90 = strel('line',2,90);
se0 = strel('line',2,0);

BWsdil = imdilate(BWs,[se90 se0]);
BWdfill = imfill(BWsdil,'holes');

BW_filt=bwareafilt(logical(BWdfill),1);
ROI = regionprops(BW_filt,'Centroid','Area','BoundingBox','MajorAxisLength','MinorAxisLength','Image','Circularity','PixelList');

BW_filt=circshift(BW_filt,[5,5]);

% subplot(1,1,1)
% im_mask=labeloverlay(Im,BW_filt);
% imshow(im_mask);
% pause(0.1)
% break

% subplot(1,1,1)
% imshow(ROI.Image);
% pause

Im_final=zeros( size(Im,1) , size(Im,2));
for i=1: size(ROI.PixelList,1)

    Im_final(ROI.PixelList(i,2),ROI.PixelList(i,1))=Im(ROI.PixelList(i,2),ROI.PixelList(i,1));

end

win_size_x=ROI.BoundingBox(3)/2+3;
win_size_y=20;

V_quad= Im_final ( floor(ROI.Centroid(2)-win_size_y) : floor(ROI.Centroid(2)+win_size_y) , ...
                     floor(ROI.Centroid(1)): floor(ROI.Centroid(1)+win_size_x)     );


%%%%
% subplot(1,1,1)
% imshow(uint8(Im_final));
% rectangle("Position",[floor(ROI.Centroid(1)), floor(ROI.Centroid(2)-win_size_y), win_size_x, 2*win_size_y],'EdgeColor','y');
% pause
% break


profile=mean(V_quad,1);



[Minima,MinIdx]=islocalmin(profile,'MinProminence',10);
min_pos=Minima.*profile;



%%%%
% subplot(2,1,1)
% plot(profile);
% hold on
% plot(min_pos);
% pause(1)
% break

for i=size(profile,2):-1:1
  
    if  profile(1,i) > 0
        store_edge_pos=[i profile(1,i)];
        break
    end

end


store=0;

for s=store_edge_pos(1,1)-gap:-1:1
   if min_pos(1,s) < lim_lumen && min_pos(1,s)>10
   
       store_min=[s min_pos(1,s)];
       store=store+1;   
       
       break        
   end
end

V_rot0=[size(Im_final,2)/2 ; size(Im_final,1)/2];

if store==0

    thickness(st,:)=[rot n abs( store_min(1,1)-store_edge_pos(1,1) ) store_edge_pos(1,1) (ROI.MajorAxisLength+ROI.MinorAxisLength)/2 0];

    vect_xy_1=[ store_min(:,1)+floor(ROI.Centroid(1))    ; 
          size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y) ]-V_rot0;

    vect_xy_2=[ store_edge_pos(1)+floor(ROI.Centroid(1))    ; 
          size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y) ] -V_rot0;


else

    thickness(st,:)=[rot n abs( store_min(1,1)-store_edge_pos(1,1) ) store_edge_pos(1,1) (ROI.MajorAxisLength+ROI.MinorAxisLength)/2 1];

    vect_xy_1=[ store_min(:,1)+floor(ROI.Centroid(1))    ; 
          size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y) ] -V_rot0 ;

    vect_xy_2=[store_edge_pos(1)+floor(ROI.Centroid(1))   ; 
          size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)] - V_rot0;

    

end
st=st+1;


%%%% plot section
%
% 
% subplot(2,1,1)
% imshow(uint8(Im_final));
% rectangle("Position",[floor(ROI.Centroid(1)), floor(ROI.Centroid(2)-win_size_y), win_size_x, 2*win_size_y],'EdgeColor','y');
% hold on
% if store ==0
% line([ store_min(:,1)+floor(ROI.Centroid(1))   store_edge_pos(1)+floor(ROI.Centroid(1)) ],[size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)   size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)],'Color','r')
% else
% line([ store_min(:,1)+floor(ROI.Centroid(1))   store_edge_pos(1)+floor(ROI.Centroid(1)) ],[size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)   size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)],'Color','g')
% end

% rectangle("Position",[ROI.BoundingBox(1), ROI.BoundingBox(2), ROI.BoundingBox(3), ROI.BoundingBox(4)],'EdgeColor','y');

subplot(2,1,1)
plot(min_pos,'s');
hold on
plot(store_min(:,1),store_min(:,2),'*');
hold on
plot(profile);
grid on
ylim([0,150]);
pause(0.001);
hold off

vect_rot_1 = [cos(rot*pi/180) -sin(rot*pi/180) ; sin(rot*pi/180) cos(rot*pi/180)]*vect_xy_1;
vect_rot_2 = [cos(rot*pi/180) -sin(rot*pi/180) ; sin(rot*pi/180) cos(rot*pi/180)]*vect_xy_2;

subplot(2,1,2)

if rot==rot_start
imshow(uint8(V));
hold on
end


if store==0
line([ vect_rot_1(1,1)+V_rot0(1,1)   vect_rot_2(1,1)+V_rot0(1,1) ],[ vect_rot_1(2,1)+V_rot0(2,1)    vect_rot_2(2,1)+V_rot0(2,1)  ],'Color','r');
hold on
else
line([ vect_rot_1(1,1)+V_rot0(1,1)   vect_rot_2(1,1)+V_rot0(1,1) ],[ vect_rot_1(2,1)+V_rot0(2,1)    vect_rot_2(2,1)+V_rot0(2,1)  ],'Color','g'); 
hold on
end
pause(0.000001)
title(strcat(int2str(fr)));
 

end


saveas(f,strcat(folder_save,'\frame_',num2str(fr),'.tif'));
close all

end
toc



%% EXTRACT DATA TO PLOT


n_start=1;
% frame_interval=15;

i=n_start;
st=1;
t_thick=[];
t_store=[];
% thickness=Data;

while i<=max(thickness(:,2))

[val,index]=find(thickness(:,2)==i);

t_store=thickness(val(1):val(end),:);


out = t_store(all(t_store,2),:);

%%% column 3 is thickness and column 4 is outer radius

t_thick(st,:)=[i mean(out(:,3)) std(out(:,3))  median(out(:,4))  std(out(:,4)) mean(out(:,4)-out(:,3)) std(out(:,4)-out(:,3)) ...
                 median( 4/3*pi* (out(:,4)-out(:,3)).^3)  std(4/3*pi* (out(:,4)-out(:,3)).^3) ...
                 median( 4/3*pi* ( out(:,4)).^3 - (out(:,4) - out(:,3)).^3 )   std(4/3*pi* ( out(:,4)).^3 - (out(:,4) - out(:,3)).^3)];

%%% column 2 is thickness,|| column 4 is outer radius || column 6 is inner
%%% radius || column 8 is lumen volume || column 10 is cyst cellular volume.

st=st+1;
i=i+frame_interval;


end


%% PLOT SECTION

% t_thick=load("t_thick.mat").t_thick;

lim=48;
start=1;

x_plot=t_thick(start:lim,1);


y_plot=t_thick(start:lim,10);
y_err1=t_thick(start:lim,10+1);
% y_err2=t_thick(1:1:end,6+1);

figure

y_low=(y_plot)+y_err1;
y_high=(y_plot)-y_err1;

% plot((x_plot), movmean(y_low,2) , '-','MarkerFaceColor','b'  ,'MarkerSize',8)
% hold on
% plot((x_plot), movmean(y_high,2) , '-','MarkerFaceColor','g'  ,'MarkerSize',8)
% hold on

% area((x_plot)-1, movmean(y_low/y_plot(1),2));
% hold on
% area((x_plot)-1, movmean(y_high/y_plot(1),2));
hold on
% e1=errorbar((x_plot)-1,  (y_plot)/y_plot(1),  (y_err1)/y_plot(1), '-','MarkerFaceColor','b'  ,'MarkerSize',8);

e1=plot((x_plot)-1,  (y_plot)/y_plot(1), '-s','MarkerFaceColor','b'  ,'MarkerSize',8);
hold on
% e1.CapSize=0;

% y=fit(x_plot-1, y_plot/y_plot(1), 'exp1');
% x=linspace(x_plot(1)-1,x_plot(end)-1,50);
% 
% %
% cf=coeffvalues(y);
% %
% plot_y=cf(1)*exp(cf(2)*x);
% % plot_y=
% plot((x),plot_y,'-.','LineWidth',2);

set(findall(gcf,'-property','FontSize'),'FontSize',34)
        set(gcf,'units','points','position',[411.5,125,480,400.5]);

xlabel('h');
ylabel('r ');


%
% y_low=(y_plot)+y_plot;
% y_high=(y_plot)-y_err1;
% 
% % plot((x_plot), y_low  , '-','MarkerFaceColor','b'  ,'MarkerSize',8)
% % hold on
% % plot((x_plot), y_high  , '-','MarkerFaceColor','g'  ,'MarkerSize',8)
% % hold on
% plot(log((x_plot)*scale),  log((y_plot)*scale),'s','MarkerFaceColor','b'  ,'MarkerSize',8,'LineWidth',2)
% % plot((x_plot*scale),  (y_plot*scale),'s','MarkerFaceColor','b','MarkerSize',8);
% set(findall(gcf,'-property','FontSize'),'FontSize',34)
%         set(gcf,'units','points','position',[811.5,225,480,400.5]);
% xlabel('t (s)');
% ylabel('h/h_0 (um)');
% hold on
% %
% %
% hold on
% e1=errorbar((x_plot),   (y_plot),  (y_err2), 'horizontal','s','MarkerFaceColor','b','MarkerSize',8);
% e1.CapSize=0;
% %
% y=fit(x_plot, y_plot, 'power1');
% x=linspace(x_plot(1),x_plot(end),50);
% set(findall(gcf,'-property','FontSize'),'FontSize',24)
%         set(gcf,'units','points','position',[811.5,225,480,400.5]);
% %
% cf=coeffvalues(y)
% %
% plot_y=cf(1)*x.^cf(2);
% 
% plot((x),plot_y,'-.','LineWidth',2);
% 
% set(findall(gcf,'-property','FontSize'),'FontSize',24)
%         set(gcf,'units','points','position',[811.5,225,480,400.5]);
% 
