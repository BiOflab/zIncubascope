%%% Run this to extract the volume date of each pixel for each capsule with
%%% the correct strel element size to ensure that the mask of the yeast
%%% aggregates are well accounted for

clear all

file='BF_1_vid-6';
Vid=VideoReader(strcat(file,'.avi'));

Vid_Mask= tiffreadVolume('MASK_BF_full-6.tif');

folder_save='C:\Users\Anirban\Desktop\Incubascope Data\yeast_capsule_27092023\analyiss\analyzed_global threshold';

% figure
tic
ref_intensity=142;

for fr=1:55 
% f=figure
V=read(Vid,fr);
Im=squeeze(V(:,:,1));

BWs=Vid_Mask(:,:,fr);

se90 = strel('line',5,90);
se0 = strel('line',5,0);

BWsdil = imdilate(BWs,[se90 se0]);
BWdfill = BWsdil; %imfill(BWsdil,'holes');

BWdfill=imclearborder(BWdfill);

BW_filt=bwareafilt(logical(BWdfill),1);

ROI(fr,:) = regionprops(BW_filt,'Centroid','Area','BoundingBox','MajorAxisLength','MinorAxisLength','Image', ...
                            'Circularity','PixelList');



for i=1: size(ROI(fr,1).PixelList,1)

    vol_pixel(fr,i,:)=[ROI(fr,1).PixelList(i,2), ROI(fr,1).PixelList(i,1),  double(Im(ROI(fr,1).PixelList(i,2),ROI(fr,1).PixelList(i,1))),  log( ref_intensity/double(Im(ROI(fr,1).PixelList(i,2),ROI(fr,1).PixelList(i,1))) )];
    

end


% subplot(1,1,1)
% im_mask=labeloverlay(Im,BW_filt,'Transparency',0.75);
% imshow(Im_final);
% title(int2str(fr));
% pause
% break

% saveas(f,strcat(folder_save,'\frame_',num2str(fr),'.tif'));
% close all

end

save(strcat(file,'_vol_pixels.mat'),"vol_pixel",'-mat');
toc


%%

%%%% estimate volume at each time step by summing up the volumes of pixels and plot

color=['y','b','g','r','k',{'m'},'c'];
figure
lim=50;
start=3;

Y_store=[];

x_plot=((0:15:15*(lim-start)))'+30;
for video_num=1:6

vol_pixel=load(strcat('BF_1_vid-',int2str(video_num),'_vol_pixels.mat')).vol_pixel;

for fr=1:55

    volume(fr)=sum(abs([vol_pixel(fr,:,4)]));
end


plot(x_plot,volume(3:50)/volume(2),':','Color',color{video_num},'LineWidth',3);
hold on

Y_store=[Y_store ,(volume(3:50)./volume(2))'];

volume=[];

end

set(findall(gcf,'-property','FontSize'),'FontSize',34)
set(gcf,'units','points','position',[811.5,225,480,400.5]);

