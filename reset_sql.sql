use test_arham;

delete from userrolemapping where user_id>0 ;
delete from user where id>0;
delete from useraddress where address_id>0;

delete  from userprofile where profile_id>0;

delete from submenumaster where submenu_id>0;
delete from menumaster where menu_id>0;

alter table user  AUTO_INCREMENT=1;
alter table userrolemapping  AUTO_INCREMENT=1;
alter table useraddress  AUTO_INCREMENT=1;
alter table userprofile  AUTO_INCREMENT=1;
alter table submenumaster  AUTO_INCREMENT=1;
alter table menumaster  AUTO_INCREMENT=1;

