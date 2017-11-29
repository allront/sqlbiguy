CREATE PROC [dbo].[SP_RefreshCBRFrates] as
declare @hDoc INT
declare @xml xml
declare @Object as Int;
declare @ResponseText as Varbinary(8000);
declare @Url as Varchar(MAX);
declare @usd float;
declare @eur float;

declare @i int
select @i=0
While @i>=-10 -- if we want to get last 10 records
BEGIN 
select @Url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='+convert(varchar(100), DATEADD(day,@i,CAST(GETDATE() as date)), 103)
Exec sp_OACreate 'MSXML2.XMLHTTP', @Object OUT;
Exec sp_OAMethod @Object, 'open', NULL, 'get', @Url, 'false'
Exec sp_OAMethod @Object, 'send'
Exec sp_OAMethod @Object, 'responsebody', @ResponseText OUTPUT
Exec sp_OADestroy @Object
SELECT @xml = cast (@ResponseText as xml)
EXEC sp_xml_preparedocument @hDoc OUTPUT,@xml
SELECT
@usd = cast(replace(value, ',','.') as float)
FROM
OPENXML(@hDoc, '//Value')
WITH
(
id nvarchar(100) '../@ID',
name nvarchar(100) '../Name',
value nvarchar(100) '../Value'
)
where id = 'R01235' --USD currency code

SELECT
@eur = cast(replace(value, ',','.') as float)
FROM
OPENXML(@hDoc, '//Value')
WITH
(
id nvarchar(100) '../@ID',
name nvarchar(100) '../Name',
value nvarchar(100) '../Value'
)
where id = 'R01239' --EUR currency code

SELECT [RepDate]=DATEADD(day,@i,CAST(GETDATE() as date)), @usd, @eur --Result String

EXEC sp_xml_removedocument @hDoc

set @i=@i-1
END
GO