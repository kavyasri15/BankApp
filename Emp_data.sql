/*	Create the final output table 	                */
/*	Import the data into the SQL database	        */
/*		and then run the procedure	                */
/*	                                                */
/*	data - The Table with all the employee data	    */
/*	temp - Temp table to iter through Employee Kins	*/
/*			one at a time                           */
/*	TempTable - temp table for approver data        */
	

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `createFinal`()
    NO SQL
begin
CREATE TABLE FINAL (
KIN                  VARCHAR(255) PRIMARY KEY,
Region               VARCHAR(255),
FIN_Region           VARCHAR(255),
First_Name           VARCHAR(255),
Middle_Name          VARCHAR(255),
Last_Name            VARCHAR(255),
NT_LOGIN_ID          VARCHAR(255),
Organization         VARCHAR(255),
Person_Type          VARCHAR(255),
Designation          VARCHAR(255),
Location             VARCHAR(255),
Base_Location        VARCHAR(255),
Entity               VARCHAR(255),
Sub_Practice         VARCHAR(255),
Supervisor_KIN       VARCHAR(255),
Supervisor_Full_Name VARCHAR(255),
Supervisor_Email_ID  VARCHAR(255),
Associate_Email_ID   VARCHAR(255),
Account              VARCHAR(255),
Project_Name         VARCHAR(255),
Project_Number       VARCHAR(255),
Associate_Full_Name  VARCHAR(255),
Skill_Group          VARCHAR(255),
LOCAL_GRADE          VARCHAR(255),
APPROVER_KIN         VARCHAR(255),
APPROVER_NAME        VARCHAR(255),
APPROVER_EMAIL       VARCHAR(255)	
);
end$$
DELIMITER ;


/* function for getting the approvers name */
DELIMITER $$
CREATE DEFINER=`root`@`localhost` FUNCTION `getApprover`(`kinId` VARCHAR(255)) RETURNS varchar(255) CHARSET latin1
    NO SQL
BEGIN
declare superkin varchar(255);
declare iter integer(10);
declare grade varchar(10);
declare err varchar(10);
declare x varchar(10);
declare y varchar(10);
set err = "NO";
set iter=1;

while (iter<=5)
do
select Supervisor_KIN into superkin from emp_data.data where kin = kinId;
if found_rows()<>0 then
select LOCAL_GRADE into grade from data where kin = superkin;
set x = substring(grade,1,1);
set y = substring(grade,2,1);
if x <> 'A' and x <> 'B' and grade <> 'NULL' THEN
if x = 'C' THEN
if y <> '1' THEN
return superkin;
ELSE
set kinId = superkin;
end if;
ELSE
return superkin;
end if;
ELSE
set kinId = superkin;
end if;
ELSE
return err;
end if;
set iter = iter + 1;
if iter = 5 THEN
return err;
end if;
end while;

END$$
DELIMITER ;


/* procedure to run for all the employees */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `test`()
begin
	DECLARE tempcount integer(10);
    Declare total integer(10);
    Declare kin1 varchar(255);
    declare approver varchar(255);
    declare app_email varchar(255);
    declare app_name varchar(255);
    
	CREATE TABLE temp(
		ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		KIN VARCHAR(255) NOT NULL	
	);
    
    insert into temp (kin) select kin from data;
	
	select count(*) into total from temp;
	set tempcount = 1;
    
    while (tempcount <= total)
    DO
    	select kin into kin1 from temp where id = tempcount;
        #set kin1 = '103246_FS';     
        #select getApprover(kin1) into approver;
        set approver = getApprover(kin1);
        set app_name = NULL;
        set app_email = NULL;
        if approver <> "NO" then        	
        	select Associate_Email_ID,
            		First_Name
            into app_email,
            	app_name
            from data
            where
            kin = approver;
        	CREATE TEMPORARY TABLE TempTable
            as
            select kin1, approver, app_name, app_email;
        	insert into FINAL
            select e.*,
            a.approver, a.app_name, a.app_email
            from data as e
            left join TempTable as a
            on e.kin = a.kin1 where kin = kin1;        
        end if;
        set tempcount = tempcount + 1; 
        drop temporary table if exists TempTable;
	end while; 
end$$
DELIMITER ;
