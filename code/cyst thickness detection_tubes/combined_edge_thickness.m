%%
clear all
Vid=VideoReader('BF-D4_2.avi');


Vid_Mask= tiffreadVolume('MASK_BF-D4_2.tif');

% VideoReader('MASK_hypoosmotic shock.avi');

% V_m=read(Vid,1);

folder_save='C:\Users\Anirban\Desktop\Incubascope Data\tubes 0.8M';
%
st=1;

rot=39;

%%
f=figure;

for fr=1:1:23
    n=fr;

% BWs_plot=Vid_plot(:,:,fr);
% 
% se90 = strel('line',2,90);
% se0 = strel('line',2,0);
% 
% BWsdil = imdilate(BWs_plot,[se90 se0]);
% BWsdil=imclearborder(BWsdil);
% % BWdfill = imfill(BWsdil,'holes');
% BWdfill=BWsdil;
% BW_filt_plot=bwareafilt(logical(BWdfill),1);
% % imshow((BWdfill));
% % pause
% ROI_0 = regionprops(BW_filt_plot,'Centroid','Area');
    


V=read(Vid,fr);
V=squeeze(V(:,:,1));


Im=V;
Im=imrotate(Im,rot,'crop');

BWs=Vid_Mask(:,:,fr);
BWs=imrotate(BWs,rot,'crop');

se90 = strel('line',2,90);
se0 = strel('line',2,0);

BWsdil = imdilate(BWs,[se90 se0]);
BWdfill = imfill(BWsdil,'holes');

BW_filt=bwareafilt(logical(BWdfill),1);

% im_mask=labeloverlay(Im,BW_filt);
% imshow(im_mask);


ROI = regionprops(BW_filt,'Centroid','Area','BoundingBox','MajorAxisLength','MinorAxisLength','Image','Circularity','PixelList','Orientation');
ROI.Centroid;


Im_final=zeros( size(Im,1) , size(Im,2));
for i=1: size(ROI.PixelList,1)

    Im_final(ROI.PixelList(i,2),ROI.PixelList(i,1))=Im(ROI.PixelList(i,2),ROI.PixelList(i,1));

end



%%%%%%  HORIZONTAL DETECTION

lim_lumen=75;
gap=30;
win_size_y=20;
win_size_x=ROI.BoundingBox(3)/2+10;

% f1=figure;

imshow(uint8(Im_final));
hold on 
plot(ROI.Centroid(1),ROI.Centroid(2),'s');
hold on
% % pause
% 
disp_start=-64;
disp_end=15;

const=0;
% 
for local=disp_start:5:disp_end

if fr>12
    const=80;
end

disp=local+const;

% disp=n*5;
% disp=0;

V_quad= Im_final ( floor(ROI.Centroid(2)-win_size_y)+disp : floor(ROI.Centroid(2)+win_size_y)+disp, ...
                     floor(ROI.Centroid(1)): floor(ROI.Centroid(1)+win_size_x)     );


profile=mean(V_quad,1);

[Minima,MinIdx]=islocalmin(profile,'MinProminence',10);
min_pos=Minima.*profile;

[A,B]=find(min_pos==0);

for i=1:size(B,2)
    min_pos(1,B(1,i))=300;
end

[min_pos_V,min_pos_I]=min(min_pos);

for i=size(profile,2):-1:1

    if V_quad(win_size_y+1,i)>20
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

if s<200
thickness_H(st,:)=[ fr disp  abs( store_min(1,1)-store_edge_pos(1,1) ) store_edge_pos(1,1) store_min(1,1) 0];
% st=st+1;
else
thickness_H(st,:)=[ fr disp  abs( store_min(1,1)-store_edge_pos(1,1) ) store_edge_pos(1,1) store_min(1,1) 1];

end

% subplot(1,1,1)
if thickness_H(st,6)==1
% line([ store_min(:,1)+floor(ROI.Centroid(1))  store_edge_pos(1)+floor(ROI.Centroid(1)) ],[size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)+disp  size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)+disp],'Color','r')
% hold all
% else
line([ store_min(:,1)+floor(ROI.Centroid(1))   store_edge_pos(1)+floor(ROI.Centroid(1))],[size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)+disp   size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)+disp],'Color','g')
end
hold on
% rectangle("Position",[ floor(ROI.Centroid(1)), floor(ROI.Centroid(2)-win_size_y)+disp,  win_size_x, 2*win_size_y],'EdgeColor','y');
% hold on



% 
% subplot(2,1,2)
% if thickness(st,6)==0
% line([ store_min(:,1)+floor(ROI.Centroid(1))-shift_x   store_edge_pos(1)+floor(ROI.Centroid(1))-shift_x ],[size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)+disp-shift_y  size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)+disp-shift_y],'Color','r')
% hold all
% else
% line([ store_min(:,1)+floor(ROI.Centroid(1))-shift_x   store_edge_pos(1)+floor(ROI.Centroid(1))-shift_x ],[size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)+disp-shift_y   size(V_quad,1)/2+floor(ROI.Centroid(2)-win_size_y)+disp-shift_y],'Color','g')
% end
% pause(1/20);


st=st+1;


end
% saveas(f1,strcat('disp_horiz_',int2str(fr)),'fig');

%%%%%% VERTICAL DETECTION


lim_lumen=60;
disp_start=-20;
disp_end=50;
gap=40;

win_size_x=20;
win_size_y=ROI.BoundingBox(4)/2+10;
%

% subplot(1,1,1)
% imshow(uint8(Im_final));
% hold on 
% plot(ROI.Centroid(1),ROI.Centroid(2),'s');
% hold on
const=220;

% f1=figure

% imshow(uint8(Im_final));
% hold on 
% plot(ROI.Centroid(1),ROI.Centroid(2),'s');
% hold on

for local=disp_start:5:disp_end




    if fr>18
     const=290;
    end
% disp=local+fr*10+100;

disp=ROI.BoundingBox(3)/2-const+local;
% disp=50+fr*10+local;
% ROI.BoundingBox(3)/2
% disp=floor(ROI.Centroid(1)+ROI.BoundingBox(3)/2)-200;

V_quad= Im_final ( floor(ROI.Centroid(2))-win_size_y : floor(ROI.Centroid(2)), ...
                     floor(ROI.Centroid(1))+disp: floor(ROI.Centroid(1)+win_size_x)+disp     );

profile=mean(V_quad,2);
% profile=profile';
[Minima,MinIdx]=islocalmin(profile,'MinProminence',10);
min_pos=Minima.*profile;


% rectangle("Position",[floor(ROI.Centroid(1))+disp, floor(ROI.Centroid(2))-win_size_y, win_size_x, win_size_y],'EdgeColor','y');
% hold on
% subplot(2,1,1)
% imshow(uint8(V_quad));
% hold on
% pause
% [A,B]=find(min_pos==0);
% 
% for i=1:size(B,2)
%     min_pos(1,B(1,i))=300;
% end
% 
% [min_pos_V,min_pos_I]=min(min_pos);

for i=1:1:size(profile,1)

    if V_quad(i,win_size_x+1)>20
        store_edge_pos=[i profile(i,1)];
        break
    end
end

store=0;
for s=store_edge_pos(1,1)+gap:1:size(profile,1)
   if min_pos(s,1) < lim_lumen && min_pos(s,1)>10

       store_min=[s min_pos(s,1)];
       store=store+1;   

       break        
   end
end


thickness_V(st,:)=[fr disp  abs( store_min(1,1)-store_edge_pos(1,1) ) store_edge_pos(1,1) store_min(1,1) 1];
% % st=st+1;
% else
% thickness_H(st,:)=[ n disp  abs( store_min(1,1)-store_edge_pos(1,1) ) store_edge_pos(1,1) store_min(1,1) 1];
% end


% line([size(V_quad,2)/2  size(V_quad,2)/2],[store_min(:,1)  store_edge_pos(1) ],'Color','r');    
% 
% % subplot(1,1,1)
if thickness_V(st,6)==1

% line([size(V_quad,2)/2+floor(ROI.Centroid(1))+disp  size(V_quad,2)/2+floor(ROI.Centroid(1))+disp],[store_min(:,1)+floor(ROI.Centroid(2))-win_size_y  store_edge_pos(1)+floor(ROI.Centroid(2))-win_size_y ],'Color','r');    
% hold all
% else
% rectangle("Position",[floor(ROI.Centroid(1))+disp, floor(ROI.Centroid(2))-win_size_y, win_size_x, win_size_y],'EdgeColor','y');
% hold on
line([size(V_quad,2)/2+floor(ROI.Centroid(1))+disp  size(V_quad,2)/2+floor(ROI.Centroid(1))+disp],[store_min(:,1)+floor(ROI.Centroid(2))-win_size_y  store_edge_pos(1)+floor(ROI.Centroid(2))-win_size_y ],'Color','y'); 
hold all
end




st=st+1;


% subplot(2,1,2)
% plot(profile);
% hold on
% plot(min_pos,'s');
% hold on
% plot(store_edge_pos(1),store_edge_pos(2),'o','MarkerFaceColor','k');
% hold on
% plot(store_min(1),store_min(2),'d','MarkerFaceColor','k');
% ylim([0,256]);
%  hold off



end

pause(0.000000000000000000001);

% saveas(f1,strcat('disp_horiz_',int2str(fr)),'fig');

% close(f1);


% close all
end


%%

thickness=thickness_V;
i=1;
frame_interval=1;
st=1;
% t_store=thickness(val(1):val(end),:);

while i<=max(thickness(:,1))

[val,index]=find(thickness(:,1)==i);

t_store=thickness(val(1):val(end),:);
% pause
 out = t_store(all(t_store,2),:);
% out=t_store;
% pause
%%% column 3 is thickness and column 4 is outer radius

t_thick(st,:)=[i median(out(:,3)) std(out(:,3))  median(out(:,4))  std(out(:,4)) median(out(:,4)-out(:,3)) std(out(:,4)-out(:,3)) ...
                 median( 4/3*pi* (out(:,4)-out(:,3)).^3)  std(4/3*pi* (out(:,4)-out(:,3)).^3) ...
                 median( 4/3*pi* ( out(:,4)).^3 - (out(:,4) - out(:,3)).^3 )   std(4/3*pi* ( out(:,4)).^3 - (out(:,4) - out(:,3)).^3)];

%%% column 2 is thickness,|| column 4 is outer radius || column 6 is inner
%%% radius || column 8 is lumen volume || column 10 is cyst cellular volume.

st=st+1;
i=i+frame_interval;
% figure
% boxplot(out(:,3),i);
% hold all
end
%
figure

plot(t_thick(:,1)*1.5-1.5,t_thick(:,2)/t_thick(1,2),'-s');

