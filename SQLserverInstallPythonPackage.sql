-- in this example we install simple_salesforce package
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

install_and_import(''simple_salesforce'')
'
