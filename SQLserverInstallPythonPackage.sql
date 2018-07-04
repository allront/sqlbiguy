CREATE PROCEDURE [dbo].[USP_InstallPythonPackage]   (@packageName nvarchar(255)) as

BEGIN

EXECUTE sp_execute_external_script    
@language = N'Python'
,@script=
N'
def install_and_import(package):
	import importlib
	try:
		importlib.import_module(package)
	except ImportError:
		import pip
		pip.main([''install'', package])
	finally:
		globals()[package] = importlib.import_module(package)

install_and_import(packageName)
'
, @params = N'@packageName nvarchar(255)'  
, @packageName = @packageName

END

-- to call USP for e.g. install simple_salesforce package type [tech].[USP_InstallPythonPackage] 'simple_salesforce'

